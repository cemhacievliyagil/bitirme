from urllib import request
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests as rq
import urllib.request
import json
import csv

aylar = {'Ocak' : '01', 'Şubat': '02', 'Mart' : '03', 'Nisan': '04', 'Mayıs' : '05', 'Haziran': '06', 'Temmuz' : '07', 'Ağustos': '08', 'Eylül' : '09', 'Ekim': '10', 'Kasım' : '11', 'Aralık': '12'}
def linkDuzelt(res):
    linkler = []       
    for link in res: 
        if link['href'] is None or link['href'] == '':   
            continue      
        if link['href'].split('/')[-2].split('-')[-1].isnumeric() and '/yazarlar/' not in link['href']:                                 
            linkler.append(link['href'])                                                      
    linkler = list(dict.fromkeys(linkler))
    return linkler

def tarihBul(soup):  
    tarih = soup.find('time') 
    if tarih.has_attr('datetime'):
        tarih = (str(tarih['datetime']).split('T')[0]).split('-')
        tarih = tarih[0] + '-' + tarih[1] + '-' +tarih[2]
    else:
        tarih = tarih.text.split()
        tarih = tarih[4] + '-' + aylar[tarih[3]] + '-' + tarih[2]
    return tarih


def spider(url, kategori):
    data = []
    try:
        r = rq.get(url)               
        soup = bs(r.content, "html.parser")               
        all_link = soup.find_all('a', class_ = 'news-item-title')                          
        linkler = linkDuzelt(all_link)       
        for link in linkler: 
            try:                        
                r = rq.get(link)               
                soup = bs(r.content, "html.parser")              
                baslik = soup.find('h1').text
                altBaslik = ''
                if soup.find('h2') is not None:
                    altBaslik = soup.find('h2').text                     
                metin = soup.find_all('p', class_ = False)
                asil = altBaslik                       
                for met in metin:
                    asil = asil + ' ' + met.text                      
                data.append(['Sözcü',link, kategori, baslik, asil, tarihBul(soup)])        
            except Exception:
                continue

    except Exception:
        spider(url, kategori)
    header = ['site','link', 'kategori', 'başlık', 'text', 'tarih','key1','key2','key3','key4','key5']
    filename = 'Haberler.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerows(data) # 5. write the rest of the data  

sections = ["https://www.sozcu.com.tr/kategori/gundem", "https://www.sozcu.com.tr/spor", 
"https://www.sozcu.com.tr/kategori/dunya","https://www.sozcu.com.tr/hayatim/magazin-haberleri",
"https://www.sozcu.com.tr/kategori/saglik","https://www.sozcu.com.tr/kategori/egitim","https://www.sozcu.com.tr/spor/futbol",
"https://www.sozcu.com.tr/spor/basketbol", "https://www.sozcu.com.tr/kategori/otomotiv", "https://www.sozcu.com.tr/hayatim/kultur-sanat-haberleri",
"https://www.sozcu.com.tr/kategori/teknoloji"]

kategori = ['Gündem', 'Spor','Dünya','Magazin','Sağlık','Eğitim','Futbol','Basketbol','Otomobil', 'Kültür-Sanat','Teknoloji']
def Sozcu():
    i = 0
    for section in sections:
        spider(section, kategori[i])
        i += 1 
