#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:36:51 2022

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

def bmj():
        nlist=[]
        urlList = ["https://www.bmj.com/news/news?category=News","https://www.bmj.com/news/feature","https://www.bmj.com/news/editorial","https://www.bmj.com/news/analysis","https://www.bmj.com/news/observations"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("a",{"data-testid":"article-entry-link"})
           for i in mya:
               URL = "https://www.bmj.com"+i["href"]
               page = requests.get(URL)    
               soup = BeautifulSoup(page.content, "html.parser")
               title= soup.find_all("h1",{"id":"page-title"})
               publD = soup.find_all("span",{"class":"highwire-cite-date"})
               cont = soup.find_all("li",{"id":"contrib-1"})
               desc1 = soup.find_all("p",{"id":"p-1"})
               desc2 = soup.find_all("p",{"id":"p-2"})
               for j,k,l,m,n in zip(title,publD,cont,desc1,desc2):
                   d={}
                   d["imageUrl"] = ""
                   d["title"] = j.text.strip()
                   d["sourceName"] = "bmj"
                   d["author"] = l.text.strip()
                   print(k.text.strip()[12:])
                   try:
                       datetime_object = datetime.datetime.strptime(k.text.strip()[12:], '%d %B %Y')
                       d["publishedAt"] = datetime_object
                       d["description"] = m.text.strip() +" "+ n.text.strip()
                       d["addedOn"] = datetime.datetime.today()
                       collection_name.insert_one(d)
                   except:
                       datetime_object = datetime.datetime.strptime(k.text.strip()[12:-1], '%d %B %Y')
                       d["publishedAt"] = datetime_object
                       d["description"] = m.text.strip() +" "+ n.text.strip()
                       d["addedOn"] = datetime.datetime.today()
                       collection_name.insert_one(d)
                   nlist.append(d)

bmj()