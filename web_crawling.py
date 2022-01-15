import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests as rq
import datetime
import urllib.request
import csv
from deneme import funct
import deneme
sections = ["https://www.haberturk.com/saglik"]
urls = []
yazilar = []
bos = ""
body_text_big = ""
for section in sections:
        try:
            newurl = section
            html = urllib.request.urlopen(newurl).read().decode("utf-8")
            
            soup = bs(html, "html.parser")
            tags = soup.find_all("div", {'class':'last-minute-area'})
            for link in tags:
                urlx = "https://www.haberturk.com" + link.a['href']
                print(urlx)
                htmlx = urllib.request.urlopen(urlx).read().decode("utf-8")
                soupx = bs(htmlx,'lxml')
                for x in soupx.find_all():
                  if len(x.get_text(strip =True)) ==0 :
                    x.extract()
                table = soupx.find('article',attrs={"class":["content type1","content type1 photo-section"]}).find_all('p')
                #external_span = soupx.find('span')
                count =0
                bos = ""
                for a in table:
                    text = a.get_text()
                    bos+=text
                    count+=1
                    if(count == len(table)):
                     yazilar.append(bos)
        except IndexError:
            break
print(len(yazilar))
for i in yazilar:
    #model_process(i.replace("\\",""))
    funct(i.replace("\\",""))
    print("-----------------------------------------------------")
            #last-minute-area
            #owl-wrapper-outer
            #gallery-container