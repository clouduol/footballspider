#! /usr/bin/python3
# page url format: https://www.dongqiudi.com/data?competition=...&type=...
#       competition=^\d+$ type=[team_rank | goal_rank | assist_rank]
# 38 * 3 = 114 

import pymysql
import re
import os
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

# parameters
seed_page = "https://www.dongqiudi.com/data"
page_types = ["team_rank","goal_rank","assist_rank"]
html_base_path = "/home/guoyunlong/workspace/footballspider/ImageSpider/data/html/data/"
image_base_path = "/home/guoyunlong/workspace/footballspider/ImageSpider/data/image/data/"

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
def  store_html(bsObj,url):
    local_path = url.replace("https://www.dongqiudi.com/","")
    local_path = local_path.split("/")[-1]
    if not local_path.endswith(".html"):
        local_path = local_path + ".html"
    title = strip_space(bsObj.find("title").get_text())
    local_path = html_base_path + title + "_" + local_path
    with open(local_path,'wt') as f:
        f.write(str(bsObj))
    return local_path

# parse seed page, get title and competition number
def parse_seed_page(bsObj):
    # title
    title = strip_space(bsObj.find("title").get_text())
    # competition number
    links = bsObj.find("div",{"id":"stat_list"}).findAll("a")
    comp_map = {}
    for link in links:
        comp_num = link.attrs['href'].split("=")[-1]
        comp_desc = strip_space(link.get_text())
        comp_map[comp_num] = comp_desc
    return [title ,comp_map]

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

# parse page, get image links and descriptions
def parse_page(bsObj):
    title = strip_space(bsObj.find("title").get_text())
    img_tags = \
    bsObj.findAll("img",{"src":re.compile("^http://img.dongqiudi.com/data")})
    link_map={}
    for img_tag in img_tags:
        link = img_tag.attrs['src']
        dsc = strip_space(img_tag.parent.get_text())
        link_map[link] = dsc
    return [title,link_map]

# main function
if __name__ == "__main__":
    # process seed page
    print("process seed page")
    html = urlopen(seed_page)
    bsObj = BeautifulSoup(html,"lxml")
    [title,comp_map] = parse_seed_page(bsObj)
    if not query_if_store("pages",seed_page):
        local_path = store_html(bsObj,seed_page)
        store_page(seed_page,title,local_path)
    # create image dirs
    print("create image dirs")
    for comp_num,comp_desc in comp_map.items():
        img_dir = image_base_path + comp_desc
        if not os.path.exists(img_dir):
           os.makedirs(img_dir)
        for page_type in page_types:
            img_sub_dir = img_dir + "/" + page_type
            if not os.path.exists(img_sub_dir):
                os.makedirs(img_sub_dir)
    # form urls
    print("form urls")
    urls = []
    for comp_num in comp_map:
        for page_type in page_types:
            url = \
            "https://www.dongqiudi.com/data?competition="+comp_num+"&type="+page_type
            urls.append(url)

    # parse page
    print("start parse page")
    succeed_count = 0
    try:
        # parse all pages
        while(len(urls)):
            for url in urls:
                try:
                    print("processing %s ..." %url)
                    if query_if_store("pages",url):
                        # pop url
                        urls.remove(url)
                        succeed_count = succeed_count + 1
                        print( \
                            "Already proccesed, skip,successfulcount:"+str(succeed_count)) 
                        continue
                    html = urlopen(url)
                    bsObj = BeautifulSoup(html,"lxml")
                    local_path = store_html(bsObj,url)
                    [title,link_map] = parse_page(bsObj)
                    # parse all images in one page, at most 10 times
                    links = list(link_map.keys())
                    left_time = 10
                    while(left_time):
                        print("left image count:%s\tleft time:%s" % \
                              (str(len(links)),str(left_time)))
                        left_time = left_time - 1
                        for link in links:
                            try:
                                if query_if_store("images",link):
                                    # pop link
                                    links.remove(link)
                                    continue
                                # print("image link :" + link)
                                dsc = link_map[link]
                                img_name = dsc+"_"+link.split("/")[-1]
                                page_type = url.split("=")[-1]
                                comp_num = url.split("&")[0].split("=")[-1]
                                img_local_path = \
                                image_base_path+comp_map[comp_num]+"/"+page_type+"/"+img_name
                                urlretrieve(link,img_local_path)
                                store_image(link,dsc,img_local_path,url)
                                # pop link
                                links.remove(link)
                            except Exception as e:
                                # print("Exception:%s" %e)
                                pass
                    store_page(url,title,local_path)
                    # pop url
                    urls.remove(url)
                    succeed_count = succeed_count + 1
                    print( \
                        "processing succeed! successful count:"+str(succeed_count))
                except Exception as e:
                    print("exception found:%s" % e)
                    pass
        print("Parse All Pages Successfully, Congratulations!")
    finally:
        cur.close()
        conn.close()
