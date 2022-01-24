#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:43:35 2022

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
def researchgate():

        nlist=[]
        urlList = ["https://www.researchgate.net/blog"]
        for h in urlList:
               URLM = h
               page = requests.get(URLM)
               soup = BeautifulSoup(page.content, "html.parser")
               mya = soup.find_all("h1",{"class":"nova-legacy-e-text"})
               img = soup.find_all("a",{"class":"link-image"})
               for i,j in zip(mya,img):
                       img = j.find("img").get('src','')
                       title = i.find("a").text.strip()
                       url = i.find("a")
                       URL = url["href"]
                       page = requests.get(URL)    
                       soup = BeautifulSoup(page.content, "html.parser")
                       imgs=img
                       author = soup.find("div",{"class":"post-body"}).text.strip().split("\n")[0]
                       publD = soup.find("div",{"class":"post-date"})
                       source = "researchgate"
                       summary = soup.find("div",{"class":"post-body"}).text.strip().split("\n")[2]
                       d={}
                       d["imageUrl"] = imgs
                       d["title"] = title
                       d["sourceName"] = source
                       d["author"] = author
                       d["description"] = summary
                       d["addedOn"] = datetime.datetime.today()
                       if len(publD.text.strip().split(" "))>2:
                           if len(publD.text.strip().split(" ")[0])==3:
                               datetime_object = datetime.datetime.strptime(publD.text.strip().split(" ")[0][:1]+" "+publD.text.strip().split(" ")[1]+" "+publD.text.strip().split(" ")[2], '%d %B %Y')
                           if len(publD.text.strip().split(" ")[0])==4:
                               datetime_object = datetime.datetime.strptime(publD.text.strip().split(" ")[0][:2]+" "+publD.text.strip().split(" ")[1]+" "+publD.text.strip().split(" ")[2], '%d %B %Y')
                           d["publishedAt"] = datetime_object
                           collection_name.insert_one(d)

researchgate()