import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests as rq
import datetime
import urllib.request
import csv
sections = ["https://www.haberturk.com/saglik"]
urls = []
yazilar = []
yazi = ""
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
                table = soupx.find('article',attrs={"class":"content type1"}).findAll('p')
                external_span = soupx.find('span')
                for x in table:
                  yazilar.append(x.getText())
                print(yazilar)
        except IndexError:
            break

with open('quotes.txt','a') as f:
            for i in range(len(tags)):
                f.write(str(tags[i].encode("utf-8"))+' '+str(tags[i].encode("utf-8"))+'\n')
urldata = pd.DataFrame(tags)

urldata.head()
urldata = urldata.drop_duplicates()
urldata.to_csv('urldata.csv')
            #last-minute-area
            #owl-wrapper-outer
            #gallery-container