from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
def getTitle(url):
	try:
		html=urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html,"lxml")
		title = bsObj.title
	except AttributeError as e:
		return None
	return title

title = getTitle("https://www.dongqiudi.com")
if title == None:
	print("Title could not be found")
else:
	print(title)
