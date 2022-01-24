#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:42:46 2022

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

def medscape():

        nlist=[]
        urlList = ["https://www.medscape.com/index/list_13470_0","https://www.medscape.com/index/list_13501_0"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("li")
           for i in mya:
                   url = i.find("a",{"class":"title"})
                   title = i.find("a",{"class":"title"})
                   summary= i.find("span",{"class":"teaser"})
                   sPD = i.find("div",{"class":"byline"})
                   if sPD != None:
                       source = sPD.text.strip().split(",")[0]
                       publD = sPD.text.strip().split(",")[1]+","+sPD.text.strip().split(",")[2]
                   img = ''
                   URL = ''
                   if url != None and img != None:
                       URL = "https://www.medicalnewstoday.com/"+url.get("href",'')
                       imgs= img
                       author = ""
                       title= title.text.strip()
                       publD = publD
                       source = source
                       summary = summary.text.strip()
                       d={}
                       d["imageUrl"] = imgs
                       d["title"] = title
                       d["sourceName"] = source
                       d["author"] = author
                       d["description"] = summary
                       npd = publD.strip()
                       datetime_object = datetime.datetime.strptime(npd.strip(), '%B %d, %Y' )
                       d["publishedAt"] = datetime_object
                       d["addedOn"] = datetime.datetime.today()
                       collection_name.insert_one(d)
                       nlist.append(d)

medscape()