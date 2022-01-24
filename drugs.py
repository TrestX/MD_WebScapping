#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:39:38 2022

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

def drug():
        nlist=[]
        urlList = ["https://www.drugs.com/medical-news.html"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("div",{"class":"ddc-media"})
           for i in mya:
               imgs=i.find("figure",{"class":"ddc-embed-image"})
               title= i.find("h2",{"class":"ddc-media-title"})
               desc1 = i.find("p")
               URL = "https://www.drugs.com"+i.find("a")["href"]
               page = requests.get(URL)    
               soup1 = BeautifulSoup(page.content, "html.parser")
               d={}
               d["imageUrl"] = imgs["data-background-image"]
               d["title"] = title.text.strip()
               d["sourceName"] = "drugs"
               d["author"] = soup1.find("p",{"class":"ddc-reviewed-by"})
               npd = desc1.text.strip().split("--")[0].split(",")[1]+desc1.text.strip().split("--")[0].split(",")[2]
               datetime_object = datetime.datetime.strptime(npd.strip(), '%b %d %Y')
               d["publishedAt"] = datetime_object
               d["description"] = desc1.text.strip().split("--")[1]
               d["addedOn"] = datetime.datetime.today()
               collection_name.insert_one(d)
               nlist.append(d)

drug()