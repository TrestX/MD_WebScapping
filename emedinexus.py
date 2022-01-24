#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:36:07 2022

@author: adsorbentkarma
"""
#emedinexus

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


def emedinexus():
        nlist=[]
        for r in range(1,10):
           n=r
           URL = "https://www.emedinexus.com/section.php?page="+str(n)+"&sec=News%20and%20Updates"
           page = requests.get(URL)
           soup = BeautifulSoup(page.content, "html.parser")
           mydivs = soup.find_all("div", {"class": "news"})
           for i in mydivs:
                   img = i.find_all("img")
                   h = i.find_all("b")
                   sntd = i.find_all("span")
                   x = [sntd[i:i + 4] for i in range(0, len(sntd), 4)] 
                   for (j,k,l) in zip(img,h,x):
                       d={}
                       d["imageUrl"] = j["src"]
                       d["title"] = k.text.strip()
                       d["sourceName"] = "emedinexus"
                       npd = l[0].text.strip().split(",")[1].strip()
                       datetime_object = datetime.datetime.strptime(npd.strip(), '%d %B %Y')
                       d["publishedAt"] = datetime_object
                       d["author"] = l[0].text.strip().split(",")[0]
                       d["description"] = l[1].text.strip()
                       d["addedOn"] = datetime.datetime.today()
                       collection_name.insert_one(d)
                       nlist.append(d)
emedinexus()