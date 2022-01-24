#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:40:22 2022

@author: adsorbentkarma
"""

import requests
from bs4 import BeautifulSoup
import datetime
import pymongo
# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://mdshorts_qa_user:CHQFaW5cMFmVIQ9B@mdshorts.ecrcq.mongodb.net/mdshorts?authSource=admin&replicaSet=atlas-xwnx80-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
from pymongo import MongoClient
client = MongoClient(CONNECTION_STRING)
collection = client['mdshorts']
collection_name = collection['news']

def nih():
    
        nlist=[]
        urlList = ["https://www.nih.gov/news-events/news-releases"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("ul",{"class":"teaser-list"})
           for i in mya:
                   imgs=i.find_all("div",{"class":"teaser-thumbnail"})
                   title= i.find_all("h4",{"class":"teaser-title"})
                   desc = i.find_all("p",{"class":"teaser-description"})
                   for j,k,l in zip(imgs,title,desc):
                           d={}
                           d["imageUrl"] = j.find("img")['src']
                           d["title"] = k.text.strip()
                           d["sourceName"] = "nih"
                           d["author"] = "nih"
                           d["publishedAt"] = l.text.strip().split('\n')[0]
                           d["description"] = l.text.strip()
                           npd = l.text.strip().split('\n')[0]
                           datetime_object = datetime.datetime.strptime(npd.strip()[:-2], '%B %d, %Y' )
                           d["publishedAt"] = datetime_object
                           d["addedOn"] = datetime.datetime.today()
                           collection_name.insert_one(d)
                           nlist.append(d)

nih()