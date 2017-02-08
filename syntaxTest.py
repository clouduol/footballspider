
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html=urlopen("https://www.dongqiudi.com/data")
bsObj=BeautifulSoup(html,"lxml")

def strip_space(str):
    str=str.strip()
    str=str.strip("\t\r\n")
    str=str.replace(" ","")
    str=str.replace("\t","")
    str=str.replace("\n","")
    return str 

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
    return [title,comp_map]

links = \
bsObj.findAll("img",{"src":re.compile("^http://img.dongqiudi.com/data")})
for link in links:
    print(link.attrs['src'])
    print(strip_space(link.parent.get_text()))

