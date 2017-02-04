#! /usr/bin/python3
# crawl league rank table and store to CSV file, data in the index page of
# Dongqiudi

import csv
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

# parameter
path = "data/rank.csv"

def stripSpace(str):
    str=str.strip()
    str=str.strip("\t\r\n")
    str=str.replace(" ","")
    str=str.replace("\t","")
    str=str.replace("\n","")
    return str

html=urlopen("http://dongqiudi.com")
bsObj=BeautifulSoup(html,"lxml")
leagues=bsObj.find("div",{"id":"rank"}).findAll("a")
rankTables=bsObj.findAll("table",{"class":"cell_rank"})

csvFile=open(path,'wt',newline='')
writer=csv.writer(csvFile)

try:
    # write rank data
    for rankTable in rankTables:
        rows=rankTable.findAll("tr")
        for row in rows:
            csvRow=[]
            for cell in row.findAll(["td","th"]):
                csvRow.append(stripSpace(cell.get_text()))
            print("".join(str(x)+" " for x in csvRow))
            writer.writerow(csvRow)
finally:
    csvFile.close()
    try:
        # rename file name
        nameTail=""
        for league in leagues:
            leagueName=stripSpace(league.get_text())
            nameTail=nameTail+leagueName+"_"
        nameTail=nameTail.rstrip("_")
        nameHead=os.path.split(path)[1][:-4]
        newName=os.path.split(path)[0]+"/"+nameHead+"_"+nameTail+".csv"
        print(newName)
        os.rename(path,newName)
    except OSError as err:
        print(err)


