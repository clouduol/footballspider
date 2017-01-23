from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
html = urlopen("file:///home/guoyunlong/workspace/footballspider/index.html")
bsObj = BeautifulSoup(html, "html.parser")

count = 0
for child in bsObj.html.body.table.findAll("",limit=6):
    count=count+1
    print(count)
    print(type(child))
    print(child)
print(count)

text_list = bsObj.findAll(text=re.compile("team"),limit=1)
for text in text_list:
    print(text)
print(len(text_list))

