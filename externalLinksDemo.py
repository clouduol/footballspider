# Usage: python3 externalLinksTest [random | all] [Url]
# randomly go to another external link from one page, recursively
# get all external links from one page
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import sys

# parameter
randomExternalLinksSite = "http://www.oreilly.com"
allExternalLinksSite = "http://www.oreilly.com"

# randomization seed
random.seed(datetime.datetime.now())

# global variable
allExtLinks = set()
allIntLinks = set()

# functions
# get all internal links list, only avoid duplicated links in one page
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    # find all links starting with "/"
    for link in bsObj.findAll("a", \
                              {"href": re.compile("^(/|.*"+includeUrl+")")}):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# get all external links list, only avoid duplicated links in one page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # find all links starting with "http" or "www" and not include current url
    for link in bsObj.findAll("a", \
                    {"href": re.compile("^(http|www)((?!"+excludeUrl+").)*$")}):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

# get address part
def splitAddress(address):
    if address.startswith("http://"):
        addressParts = address.replace("http://", "").split("/")
    if address.startswith("https://"):
        addressParts = address.replace("https://", "").split("/")
    return addressParts

# get random external link
def getRandomExternalLink(startingPage):
    if not startingPage.startswith("http"):
        startingPage = "http://" + startingPage
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html,"lxml")
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    print(splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(bsObj,startingPage)
        if len(internalLinks) == 0:
            print("find zero internal link and zero external link, end")
            return ""
        return getRandomExternalLink(internalLinks[random.randint(0, \
                                                        len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0,len(externalLinks)-1)]

# follow external link from one site to another
def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    if externalLink == "":
        return
    print("random external link is : %s" % externalLink)
    followExternalOnly(externalLink)

# collect all external links , avoid duplicated links
def getAllExternalLinks(siteUrl):
    global allExtLinks
    global allIntLinks
    if not siteUrl.startswith("http"):
        siteUrl = "http://" + siteUrl 
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html,"lxml")
    internalLinks = getInternalLinks(bsObj, splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl)[0])
    print("externalLink length : " + str(len(externalLinks)))
    print("internalLink length : " + str(len(internalLinks)))
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print("external link : %s" %link)
    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            linkParts = link.split("/")
            # no "/"
            if len(linkParts)==1:
                pass
            # two or more "/" or just one link="/"
            if linkParts[0] == '' and linkParts[1]=='':
               continue 
            # one "/"
            elif linkParts[0] == '':
                link = splitAddress(siteUrl)[0] + link
            # no "/"
            else:
                pass
            print("=====> internal link : %s" % link)
            getAllExternalLinks(link)

# processing input 
if len(sys.argv) > 3:
    print("Usage: python3 externalLinksTest [random | all] [Url]")
elif sys.argv[1] == 'random':
    if len(sys.argv)==3:
        randomExternalLinksSite = sys.argv[2]
    print("type:random")
    print("Url:"+randomExternalLinksSite)
    followExternalOnly(randomExternalLinksSite)
elif sys.argv[1] == 'all':
    if len(sys.argv)==3:
        allExternalLinksSite = sys.argv[2]
    print("type:all")
    print("Url:"+allExternalLinksSite)
    getAllExternalLinks(allExternalLinksSite)
else:
    print("Usage: python3 externalLinksTest [random | all] [Url]")

