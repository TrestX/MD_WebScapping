#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:37:41 2022

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

def medpagetoday():

        nlist=[]
        urlList = ["https://www.medpagetoday.com/latest"]
        for h in urlList:
           URLM = h
           page = requests.get(URLM)
           soup = BeautifulSoup(page.content, "html.parser")
           mya = soup.find_all("div",{"class":"article_title"})
           for i in mya:
                   URL = "https://www.medpagetoday.com"+i["data-url"]
                   page = requests.get(URL)    
                   soup = BeautifulSoup(page.content, "html.parser")
                   imgs=soup.find("img",{"class":"mpt-media-container--mpt-image"})
                   title= soup.find("h1",{"class":"mpt-content-headline"})
                   publD = soup.find("span",{"class":"mpt-content-date"})
                   cont = soup.find("span",{"class":"author-name-no-email"})
                   desc1 = soup.select("div:nth-child(2) > p")[1:3]
                   d={}
                   d["imageUrl"] = imgs["src"]
                   d["title"] = title.text.strip()
                   d["sourceName"] = "medpagetoday"
                   d["author"] = cont.text.strip()
                   d["publishedAt"] = publD.text.strip()
                   d["description"] = desc1[0].text.strip()+ " "+desc1[1].text.strip()
                   npd = publD.text.strip()
                   datetime_object = datetime.datetime.strptime(npd.strip(), '%B %d, %Y' )
                   d["publishedAt"] = datetime_object
                   d["addedOn"] = datetime.datetime.today()
                   collection_name.insert_one(d)
                   nlist.append(d)

medpagetoday()