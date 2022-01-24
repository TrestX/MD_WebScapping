#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:38:30 2022

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

def medicaldialogue():
        nlist=[]
        urlList = ["https://medicaldialogues.in/medicine/news"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("article",{"class":"type-post"})
           for i in mya:
               imgs=i.find("img")
               title= i.find("h2",{"class":"title"})
               cont = i.find("div",{"class":"post-meta"})
               publD = i.find("span",{"class":"time"})
               desc1 = i.find("div",{"class":"post-summary"})
               d={}
               d["imageUrl"] = imgs["src"]
               d["title"] = title.text.strip()
               d["sourceName"] = "medpagetoday"
               d["author"] = cont.text.strip()
               d["description"] = desc1.text.strip()
               npd = publD.text.strip()[:-6]
               datetime_object = datetime.datetime.strptime(npd.strip(), '%d %b %Y %H:%M' )
               d["publishedAt"] = datetime_object
               d["addedOn"] = datetime.datetime.today()
               collection_name.insert_one(d)
               nlist.append(d)
medicaldialogue();
