#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:44:53 2022

@author: adsorbentkarma
"""

import requests
from bs4 import BeautifulSoup
import datetime 
from pymongo import MongoClient
import pymongo
# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://mdshorts_qa_user:CHQFaW5cMFmVIQ9B@mdshorts.ecrcq.mongodb.net/mdshorts?authSource=admin&replicaSet=atlas-xwnx80-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
from pymongo import MongoClient
client = MongoClient(CONNECTION_STRING)
collection = client['mdshorts']
collection_name = collection['news']

def radiopedia():
    nlist=[]
    urlList = ["https://radiopaedia.org/articles?lang=gb"]
    for h in urlList:
       URLM = h
       page = requests.get(URLM)
       soup = BeautifulSoup(page.content, "html.parser")
       mya = soup.find_all("a",{"class":"search-result search-result-article"})
       for i in mya: 
           URL = "https://radiopaedia.org"+i["href"]
           page = requests.get(URL)    
           soup = BeautifulSoup(page.content, "html.parser")
           imgs=""
           title = soup.find("h1",{"class":"header-title"})
           author = soup.find("div",{"class":"js-content content"}).find_all("a")[2]
           publD = soup.find("div",{"class":"js-content content"}).find_all("div")[12].text.strip().split(":")[1].split("by")[0]
           source = "Radiopaedia.org"
           summary = soup.find("p").text.strip()
           d={}
           d["imageUrl"] = imgs
           d["title"] = title.text.strip()
           d["sourceName"] = source
           d["author"] = author.text.strip()
           datetime_object = datetime.datetime.strptime(publD.strip(), '%d %b %Y')
           d["publishedAt"] = datetime_object
           d["description"] = summary
           d["addedOn"] = datetime.datetime.today()
           collection_name.insert_one(d)
           nlist.append(d)
radiopedia()
           