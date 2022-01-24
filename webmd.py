#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:44:11 2022

@author: adsorbentkarma
"""

import requests
from bs4 import BeautifulSoup

from datetime import date 

def webmd():
    
    nlist=[]
    urlList = ["https://www.webmd.com/news/articles"]
    for h in urlList:
       URLM = h
       page = requests.get(URLM)
       soup = BeautifulSoup(page.content, "html.parser")
       mya = soup.find_all("div")
       print(mya)
       return
       for i in mya: 
           title = i.find("a").text.strip()
           url = i.find("a")
           URL = url["href"]
           page = requests.get(URL)    
           soup = BeautifulSoup(page.content, "html.parser")
           imgs=soup.find("img")['src']
           author = soup.find("div",{"class":"byline"}).text.strip()
           publD = soup.find("p").text.strip().split("--")[0]
           sourcesl = soup.find("div",{"class":"sources__wrapper"}).find_all("p")
           source = ''
           for k in sourcesl:
               source = source + k.text.strip().split(":")[0]
           summary = soup.find("p").text.strip().split("--")[1]
           d={}
           d["imageUrl"] = imgs
           d["title"] = title
           d["sourceName"] = source
           d["author"] = author
           d["publishedAt"] = publD.text.strip()
           d["description"] = summary
           d["addedOn"] = date.today()
           nlist.append(d)
webmd()