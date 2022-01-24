#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:45:32 2022

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

def healthline():
        nlist=[]
        urlList = ["https://www.healthline.com/directory/news"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("li",{"class":"css-11kh5m1"})
           for i in mya:
               title=i.text.strip()
               imgs=i.find("lazy-image").get("src",'')
               url = i.find("a")
               URL = url["href"]
               page = requests.get(URL)    
               soup = BeautifulSoup(page.content, "html.parser")
               author = soup.find("section",{"data-testid":"byline"})
               publD = author.text.strip().split("on")[1]
               source = "healthline.com"
               summary = soup.find("p").text.strip()
               d={}
               d["imageUrl"] = imgs
               d["title"] = title
               d["sourceName"] = source
               d["author"] = author.text.strip().split("on")[0]
               npd = publD.split('—')[0].strip()
               datetime_object = datetime.datetime.strptime(npd.strip(), '%B %d, %Y')
               d["publishedAt"] = datetime_object
               d["description"] = summary
               d["addedOn"] = datetime.datetime.today()
               collection_name.insert_one(d)
               nlist.append(d)
healthline();