#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:40:53 2022

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
def newsmedical():

        nlist=[]
        urlList = ["https://www.news-medical.net/medical/news"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("h3")
           for i in mya:
                   url = i.find("a")
                   URL = "https://www.news-medical.net"+url["href"]
                   page = requests.get(URL)    
                   soup = BeautifulSoup(page.content, "html.parser")
                   imgs=""
                   author = soup.find("span",{"itemprop":"name"})
                   title= soup.find("h1",{"class":"page-title"})
                   publD = soup.find("span",{"class":"article-meta-date"})
                   source = soup.find("div",{"class":"content-src-value"})
                   summary = soup.find_all("p")
                   d={}
                   d["imageUrl"] = ''
                   d["title"] = title.text.strip()
                   d["sourceName"] = source.text.strip()
                   d["author"] = author.text.strip()
                   d["description"] = summary[1].text.strip()
                   npd = publD.text.strip()
                   datetime_object = datetime.datetime.strptime(npd.strip(), '%b %d %Y' )
                   d["publishedAt"] = datetime_object
                   d["addedOn"] = datetime.datetime.today()
                   collection_name.insert_one(d)
                   nlist.append(d)

newsmedical()
          