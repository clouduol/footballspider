from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
html = urlopen("file:///home/guoyunlong/workspace/footballspider/index.html")
bsObj = BeautifulSoup(html, "html.parser")

links = bsObj.findAll("",{"href":re.compile("^.*")})
for link in links:
    print(link)
