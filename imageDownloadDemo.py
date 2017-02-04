#! /usr/bin/python3
# get all team logo and corresponding team name in the index page of Dongqiudi
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# parameter
downloadDirectory = 'data/imageDownload'
baseUrl = 'http://img.dongqiudi.com'

def getAbsoluteURL(baseUrl,source):
    if source.startswith("http://www."):
        url="http://"+source[11:]
    elif source.startswith("https://www."):
        url="https://"+source[12:]
    elif source.startswith("http://") or source.startswith("https://"):
        url=source
    elif source.startswith("www."):
        url=source[4:]
        url="http://"+source
    else:
        source=source.lstrip('/')
        url=baseUrl+'/'+source
    #print("debug:"+url)
    #remove external links    
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path=absoluteUrl.replace("www.","")
    path=path.replace(baseUrl,"")
    path=downloadDirectory+path
    directory=os.path.dirname(path)

    # if no directory, create
    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

def imageRename(imgTag, path):
    directory=os.path.dirname(path)

    parentTag=imgTag.parent
    newName=parentTag.get_text()
    #print("old:"+newName)
    newName=newName.strip()
    newName=newName.strip("\t\r\n")
    #print("new:"+newName)

    os.rename(path,directory+'/'+newName+'.png')

if __name__ == "__main__":
    html=urlopen("http://dongqiudi.com")
    bsObj=BeautifulSoup(html,"lxml")
    imageDownloadList=bsObj.findAll("img",{"src":re.compile("^http://img.dongqiudi.com/data/")})
 
    for imageDownload in imageDownloadList:
        fileUrl=getAbsoluteURL(baseUrl,imageDownload.attrs['src'])
        if fileUrl is not None:
            print(fileUrl)
            path=getDownloadPath(baseUrl, fileUrl,downloadDirectory)
            urlretrieve(fileUrl,path)
            imageRename(imageDownload,path)

