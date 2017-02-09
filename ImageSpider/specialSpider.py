#! /usr/bin/python3
# root_page="https://www.dongqiudi.com/?tab=99&page=[1|2|3|4|5]
# special_page="https://www.dongqiudi.com/special/number number='^\d+$'
# article_page="https://www.dongqiudi.com/article/number number='^\d+$'
# img_link="http://img1.dongqiudi.com/fastdfs/..." OR
#          "http://img.dongqiudi.com/uploads[7|8|9]/allimg/..."

import pymysql
import re
import os
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

# parameters
site_name = "https://dongqiudi.com"
root_pages=["https://www.dongqiudi.com/?tab=99&page=1",\
            "https://www.dongqiudi.com/?tab=99&page=2",\
            "https://www.dongqiudi.com/?tab=99&page=3",\
            "https://www.dongqiudi.com/?tab=99&page=4",\
            "https://www.dongqiudi.com/?tab=99&page=5"]
html_base_path = \
"/home/guoyunlong/workspace/footballspider/ImageSpider/data/html/special"
image_base_path = \
"/home/guoyunlong/workspace/footballspider/ImageSpider/data/image/special"
ignore_lists = [137, 70, 138, 42, 16, 23, 10, 154, 158, 170, 176]

# database connection and cursor object
conn = \
pymysql.connect(host='127.0.0.1',unix_socket='/tmp/mysql.sock',user='root',password='root',db='mysql',charset='utf8')
cur = conn.cursor()
cur.execute("USE footballSpider")

# functions
# strip string, \s\t\r\n
def strip_space(str):
    str=str.strip()
    str=str.strip("\t\r\n")
    str=str.replace(" ","")
    str=str.replace("\t","")
    str=str.replace("\n","")
    return str

# store html file, return local path
def  store_html(bsObj,url,title,base_path):
    local_path = url.replace("https://www.dongqiudi.com/","")
    local_path = local_path.split("/")[-1]
    if not local_path.endswith(".html"):
        local_path = local_path + ".html"
    local_path = base_path + "/" +  title + "_" + local_path
    with open(local_path,'wt') as f:
        f.write(str(bsObj))
    return local_path

# parse root page, get title and special links
def parse_root_page(bsObj):
    # title
    title = strip_space(bsObj.find("title").get_text())
    # special links
    special_link_tags = bsObj.findAll("a",{"href":re.compile("^/special")})
    special_links = []
    for special_link_tag in special_link_tags:
        special_link = special_link_tag.attrs['href']
        if int(special_link.split("/")[-1]) in ignore_lists:
            continue
        special_link = site_name + special_link
        special_links.append(special_link)
    return [title ,special_links]

# parse special page, get title and article links
def parse_special_page(bsObj):
    # title
    title = strip_space(bsObj.find("h1").get_text())
    # article links
    article_link_tags = bsObj.findAll("ul")
    article_links = []
    for article_link_tag in article_link_tags:
        article_link = article_link_tag.find("a").attrs['href']
        article_link = site_name + article_link
        article_links.append(article_link)
    return [title ,article_links]

# parse article page, get title and image links
def parse_article_page(bsObj):
    # title
    title = strip_space(bsObj.find("h1").get_text())
    # image links
    image_link_tags = \
    bsObj.findAll("img",{"src":re.compile( \
                                          r"^(http:\/\/img1.dongqiudi.com\/fastdfs\/|.*allimg)")})
    image_links = []
    for image_link_tag in image_link_tags:
        image_link = image_link_tag.attrs['src']
        if image_link.startswith("/uploads"):
            image_link = "http://img.dongqiudi.com" + image_link
        image_links.append(image_link)
    return [title ,image_links]

# query to see if in database
def query_if_store(table_name,url):
    cur.execute("SELECT * FROM "+table_name+" WHERE url=%s",(url))
    if cur.rowcount == 0:
        return False
    else:
        return True

# store page
def store_page(url,title,local_path):
    cur.execute("INSERT INTO pages (url,title,local_path) VALUES \
                (%s,%s,%s)",(url,title,local_path))
    conn.commit()

# store image
def store_image(url,dsc,local_path,page_url):
    # Error:\"%s\" , 'http://www.dongqiudi.com/data'
    # redundant quote
    cur.execute("INSERT INTO images (url,dsc,local_path,page_url) VALUES \
                (%s,%s,%s,%s)",(url,dsc,local_path,page_url))
    conn.commit()


# main function
if __name__ == "__main__":
    # to close cursor and connection successfully
    try:
        # root page, to successfully process all root page 
        print("start process...")
        while(len(root_pages)):
            for root_page in root_pages:
                try:
                    print("root page: %s" % root_page)
                    # parse root page
                    root_html = urlopen(root_page)
                    root_bsObj = BeautifulSoup(root_html,"lxml")
                    [root_title,special_links] = parse_root_page(root_bsObj)
                    if not query_if_store("pages",root_page):
                        # store root page
                        root_local_path=store_html(root_bsObj,root_page,root_title,html_base_path)
                        store_page(root_page,root_title,root_local_path)
                    # special page, at most process 10 times
                    special_left_time = 10
                    while(special_left_time):
                        special_left_time = special_left_time - 1
                        for special_link in special_links:
                            try:
                                print("special link: %s" % special_link)
                                # parse special page
                                special_html = urlopen(special_link)
                                special_bsObj=BeautifulSoup(special_html,"lxml")
                                [special_title,article_links]=parse_special_page(special_bsObj)
                                # check and mkdir
                                special_html_base_path=html_base_path+"/"+special_title
                                special_image_base_path=image_base_path+"/"+special_title
                                if not os.path.exists(special_html_base_path):
                                    os.makedirs(special_html_base_path)
                                if not os.path.exists(special_image_base_path):
                                    os.makedirs(special_image_base_path)
                                if not query_if_store("pages",special_link):
                                    # store special page
                                    special_local_path=store_html(special_bsObj,special_link,special_title,special_html_base_path)
                                    store_page(special_link,special_title,special_local_path)
                                # article page, at most process 10 times
                                article_left_time = 10
                                while(article_left_time):
                                    article_left_time = article_left_time - 1
                                    for article_link in article_links:
                                        try:
                                            print("article link: %s" % \
                                                  article_link)
                                            # parse article page
                                            article_html=urlopen(article_link)
                                            article_bsObj=BeautifulSoup(article_html,"lxml")
                                            [article_title,image_links]=parse_article_page(article_bsObj)
                                            # check and mkdir
                                            article_html_base_path=special_html_base_path+"/"+article_title
                                            article_image_base_path=special_image_base_path+"/"+article_title
                                            if not os.path.exists(article_html_base_path):
                                                os.makedirs(article_html_base_path)
                                            if not os.path.exists(article_image_base_path):
                                                os.makedirs(article_image_base_path)
                                            if not\
                                            query_if_store("pages",article_link):
                                                # store article page
                                                article_local_path=store_html(article_bsObj,article_link,article_title,article_html_base_path)
                                                store_page(article_link,article_title,article_local_path)
                                            # images,at most process 10 times
                                            image_left_time = 10
                                            while(image_left_time):
                                                print(\
                                                    "left image count:%s\tleft time:%s" %\
                                                      (str(len(image_links)),str(image_left_time)))
                                                image_left_time = image_left_time-1
                                                for image_link in image_links:
                                                    try:
                                                        if\
                                                        query_if_store("images",image_link):
                                                            image_links.remove(image_link)
                                                            continue
                                                        image_name=image_link.split("/")[-1]
                                                        image_local_path=article_image_base_path+"/"+image_name
                                                        urlretrieve(image_link,image_local_path)
                                                        store_image(image_link,article_title,image_local_path,article_link)
                                                        image_links.remove(image_link)
                                                    except Exception as e:
                                                        print(\
                                                            "image exception found:%s" % e)
                                                        continue
                                            article_links.remove(article_link)
                                            print("process article successfully:%s" %\
                                                  article_link)
                                        except Exception as e:
                                            print("article page exception found:%s"
                                                  % e)
                                            continue
                                special_links.remove(special_link)
                                print("process special page successfully:%s" %\
                                      special_link)
                            except Exception as e:
                                print("special page exception found:%s" % e)
                                continue
                    root_pages.remove(root_page)
                    print("process root page successfully:%s" % root_page)
                except Exception as e:
                    print("root page exception found:%s" % e)
                    continue
                print("Congratulations! You Are Successful!")
    finally:
        cur.close()
        conn.close()
