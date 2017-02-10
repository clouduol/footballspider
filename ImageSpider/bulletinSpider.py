#! /usr/bin/python3
# Problem:  title=r'/', no such file or directory
# root_page="https://www.dongqiudi.com/?tab=1&page=[1|2|...|6658]
# article_page="https://www.dongqiudi.com/article/number number='^\d+$'
# img_link="http://img1.dongqiudi.com/fastdfs/..." OR
#          "http://img.dongqiudi.com/uploads[7|8|9]/allimg/..."

import pymysql
import re
import os
import copy
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

# parameters
site_name = "https://dongqiudi.com"
root_page_base = "https://www.dongqiudi.com/?tab=1&page="
root_page_count = 6660
html_base_path = \
"/home/guoyunlong/workspace/footballspider/ImageSpider/data/html/bulletin"
image_base_path = \
"/home/guoyunlong/workspace/footballspider/ImageSpider/data/image/bulletin"
root_html_base_path = html_base_path + "/" + "bulletin"
article_html_base_path = ""
article_image_base_path = ""

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

# get article date
def get_article_date(str):
    str=str.strip()
    str=str.strip("\t\r\n")
    str=str.split(" ")[0]
    return str

# store html file, return local path
def  store_html(bsObj,url,title,base_path):
    local_path = url.replace("https://www.dongqiudi.com/","")
    local_path = local_path.split("/")[-1]
    if not local_path.endswith(".html"):
        local_path = local_path + ".html"
    title_in_path=title
    if "/" in title:
        title_in_path = title.replace("/","_")
    local_path = base_path + "/" +  title_in_path + "_" + local_path
    with open(local_path,'wt') as f:
        f.write(str(bsObj))
    return local_path

# parse root page, get title and article links
def parse_root_page(bsObj):
    # title
    title = strip_space(bsObj.find("title").get_text())
    # article links
    article_link_tags = bsObj.find("ol").findAll("h2")
    article_links = []
    for article_link_tag in article_link_tags:
        article_link = article_link_tag.find("a").attrs['href']
        article_link = site_name + article_link
        article_links.append(article_link)
    return [title ,article_links]

# parse article page, get title,date and image links
def parse_article_page(bsObj):
    # title
    title = strip_space(bsObj.find("h1").get_text())
    # date
    article_date_tag = bsObj.find("h4").find("span",{"class":"time"})
    article_date = get_article_date(article_date_tag.get_text())
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
    return [title , article_date, image_links]

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
    # form root page
    print("form root page...")
    root_page_numbers = list(range(1, root_page_count+1))
    root_pages = []
    for root_page_number in root_page_numbers:
        root_page = root_page_base + str(root_page_number)
        root_pages.append(root_page)
    # to close cursor and connection successfully
    print("start get images...")
    try:
        root_pages_left=copy.copy(root_pages)
        # root page, at most 10 times
        root_left_time=10
        while(root_left_time):
            root_left_time=root_left_time-1
            # query, parse, process, store
            for root_link in root_pages:
                try:
                    if root_link not in root_pages_left:
                        continue
                    print("root page:%s" % root_link)
                    # root:query
                    if query_if_store("pages",root_link):
                        root_pages_left.remove(root_link)
                        print("root page already in database:%s" % root_link)
                        continue
                    # root:parse
                    root_html=urlopen(root_link)
                    root_bsObj=BeautifulSoup(root_html,"lxml")
                    root_title,article_links=parse_root_page(root_bsObj)
                    # root:process
                    article_links_left=copy.copy(article_links)
                    # article link, at most 10 times
                    article_left_time = 10
                    while(article_left_time):
                        article_left_time=article_left_time-1
                        # query, parse, process, store
                        for article_link in article_links:
                            try:
                                if article_link not in article_links_left:
                                    continue
                                print("article page:%s" % article_link)
                                # article:query 
                                if query_if_store("pages",article_link):
                                    article_links_left.remove(article_link)
                                    print("article already in database:%s"%\
                                          article_link)
                                    continue
                                # article:parse
                                article_html=urlopen(article_link)
                                article_bsObj=BeautifulSoup(article_html,"lxml")
                                article_title,article_date,image_links=parse_article_page(article_bsObj)
                                # article:process
                                article_html_base_path=html_base_path+"/"+article_date
                                article_image_base_path=image_base_path+"/"+article_date
                                if not os.path.exists(article_html_base_path):
                                    os.makedirs(article_html_base_path)
                                if not os.path.exists(article_image_base_path):
                                    os.makedirs(article_image_base_path)
                                image_links_left=copy.copy(image_links)
                                # image link, at most 10 times
                                image_left_time = 10
                                while(image_left_time):
                                    print(\
                                        "image left count:%s\timage left time:%s" %\
                                          (str(len(image_links_left)),str(image_left_time)))
                                    image_left_time=image_left_time-1
                                    # query, store
                                    for image_link in image_links:
                                        try:
                                            if image_link not in\
                                            image_links_left:
                                                continue
                                            # image:query
                                            if\
                                            query_if_store("images",image_link):
                                                image_links_left.remove(image_link)
                                                continue
                                            # image:store
                                            title_in_name=article_title
                                            if "/" in article_title:
                                                title_in_name=article_title.replace("/","_")
                                            image_name=title_in_name+"_"+image_link.split("/")[-1]
                                            image_local_path=article_image_base_path+"/"+image_name
                                            urlretrieve(image_link,image_local_path)
                                            store_image(image_link,article_title,image_local_path,article_link)
                                            image_links_left.remove(image_link)
                                        except Exception as e:
                                            print("image exception found:%s"%e)
                                            continue
                                # artile:store
                                article_local_path=store_html(article_bsObj,article_link,article_title,article_html_base_path)
                                store_page(article_link,article_title,article_local_path)
                                article_links_left.remove(article_link)
                                print("article page process successfully:%s" %\
                                      article_link)
                            except Exception as e:
                                print("article page exception found:%s" % e)
                                continue
                    # root:store
                    root_local_path=store_html(root_bsObj,root_link,root_title,root_html_base_path)
                    store_page(root_link,root_title,root_local_path)
                    root_pages_left.remove(root_link)
                    print("root page process successfully:%s" % root_link)
                except Exception as e:
                    print("root page exception found:%s" % e)
                    continue
    finally:
        cur.close()
        conn.close()
