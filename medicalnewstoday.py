#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:41:37 2022

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

def medicalnewstoday():
        nlist=[]
        urlList = ["https://www.medicalnewstoday.com/categories/allergy"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("li")
           for i in mya:
               url = i.find("a")
               title = i.find("h2")
               summary= i.find("p")
               img = i.find("lazy-image")
               URL = ''
               if url != None and img != None:
                   URL = "https://www.medicalnewstoday.com/"+url.get("href",'')
                   imgs=img.get('src','')
                   author = ""
                   title= title.text.strip()
                   publD = ""
                   source = "medical news today"
                   summary = summary.text.strip()
                   d={}
                   d["imageUrl"] = imgs
                   d["title"] = title
                   d["sourceName"] = source
                   d["author"] = author
                   d["publishedAt"] = datetime.datetime.today()
                   d["description"] = summary
                   d["addedOn"] = datetime.datetime.today()
                   collection_name.insert_one(d)
                   nlist.append(d)
               
medicalnewstoday()
