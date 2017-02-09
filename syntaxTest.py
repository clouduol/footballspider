
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html=urlopen("https://www.dongqiudi.com/article/261721")
bsObj=BeautifulSoup(html,"lxml")

def strip_space(str):
    str=str.strip()
    str=str.strip("\t\r\n")
    str=str.replace(" ","")
    str=str.replace("\t","")
    str=str.replace("\n","")
    return str

# parse special page, get title and article links
def parse_special_page(bsObj):
    # title
    title = strip_space(bsObj.find("h1").get_text())
    # article links
    article_link_tags = bsObj.findAll("ul")
    article_links = []
    for article_link_tag in article_link_tags:
        article_link = article_link_tag.find("a").attrs['href']
        article_links.append(article_link)
    return [title ,article_links]

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

[title,article_links] = parse_article_page(bsObj)
print(title)
for article_link in article_links:
    print(article_link)
