from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("https://www.dongqiudi.com")
bsObj = BeautifulSoup(html.read(),"lxml")


print("tag")
bsObj_tag = bsObj.findAll({"h1","h2","h3","h4","h5","h6"})
print("{}")
for bsTmp in bsObj_tag:
	print(bsTmp)
print(len(bsObj_tag))
bsObj_tag = bsObj.findAll(["h1","h2","h3","h4","h5","h6"])
print("[]")
for bsTmp in bsObj_tag:
	print(bsTmp)
print(len(bsObj_tag))
print("tag end")

print("attributes")
bsObj_attr = bsObj.findAll("a",{"class":[" ","sel","last"]})
for bsTmp in bsObj_attr:
	print(bsTmp)
print("attributes end")

print("recursive keywords")
bsObj_kw = bsObj.findAll(id="header")
bsObj_kw = bsObj_kw[0]
print(bsObj_kw)
print("recursive = True")
bsObj_recur = bsObj_kw.findAll("div",limit=2)
for bsTmp in bsObj_recur:
	print(bsTmp)
print(len(bsObj_recur))
print("recursive = False")
bsObj_recur = bsObj_kw.findAll("div",recursive=False)
for bsTmp in bsObj_recur:
	print(bsTmp)
print(len(bsObj_recur))
print("recursive keywords end")

print("include current node or not")
bsObj_in = bsObj.findAll("div",limit=4)
index = 0
print("bsObj_in")
for bsTmp in bsObj_in:
	print(index)
	index=index+1
	print(bsTmp)
print("bsObj_in end")
print("bsObj_in0")
bsObj_in0 = bsObj_in[0]
bsObj_in0 = bsObj_in0.findAll("div")
for bsTmp in bsObj_in0:
	print(bsTmp)
print(len(bsObj_in0))
print("bsObj_in0 end")
print("bsObj_in1")
bsObj_in1 = bsObj_in[1]
bsObj_in1 = bsObj_in1.findAll("div")
for bsTmp in bsObj_in1:
	print(bsTmp)
print(len(bsObj_in1))
print("bsObj_in1 end")
print("include current node or not end")

print("text")
bsObj_text = bsObj.findAll(text=re.compile("2017-01-22"))
for bsTmp in bsObj_text:
	print(bsTmp)
print(len(bsObj_text))
print("text end")

f=open("index.html","w+")
f.writelines(str(bsObj))
f.close()

#bsObj = bsObj.div
#print("bsObj")
#print(bsObj)
#print("bsObj end")
#print("bsObj.get_text()")
#print(bsObj.get_text())
#print("bsObj.get_text() end")
#
#teamList = bsObj.findAll("a",{"class":"nav"})
#print("node")
#for team in teamList:
#	print(team)
#print("text")
#for team in teamList:
#	print(team.get_text())
#print("count:"+str(len(teamList)))
