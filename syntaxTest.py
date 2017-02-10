
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import copy

html=urlopen("https://www.dongqiudi.com/article/274634")
bsObj=BeautifulSoup(html,"lxml")

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

site_name = "https://www.dongqiudi.com"
root_page_base = "https://www.dongqiudi.com/?tab=1&page="
root_page_count = 20

root_page_numbers = list(range(1, root_page_count+1))
root_pages = []
for root_page_number in root_page_numbers:
    root_page = root_page_number
    root_pages.append(root_page)

root_pages_left=copy.copy(root_pages)
left_time = 10
while(left_time):
    print(left_time)
    left_time=left_time-1
    for root_link in root_pages:
        if root_link not in root_pages_left:
            continue
        print(root_link)
        root_pages_left.remove(root_link)
#        print(root_pages_left)

