from urllib import request
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests as rq
import urllib.request
import json
import csv
from requests_html import HTMLSession

aylar = {'Ocak' : '01', 'Şubat': '02', 'Mart' : '03', 'Nisan': '04', 'Mayıs' : '05', 'Haziran': '06', 'Temmuz' : '07', 'Ağustos': '08', 'Eylül' : '09', 'Ekim': '10', 'Kasım' : '11', 'Aralık': '12'}
def linkDuzelt(res):
    linkler = []       
    for link in res: 
        if link['href'] is None or link['href'] == '':   
            continue      
        if link['href'][-1].isnumeric() and '/yazarlar/' not in link['href'] and '/video/' not in link['href']:
            if '.com' not in link['href']:                 
                linkler.append('https://www.hurriyet.com.tr'+link['href'])
                #print('https://www.hurriyet.com.tr'+link['href'])
            elif 'www.hurriyet' in  link['href']:
                linkler.append(link['href'])
               #print(link['href'])
                                                       
    linkler = list(dict.fromkeys(linkler))
    return linkler


def tarihBul(soup):   
    tarih = soup.find('time')  
    tarih = (str(tarih['datetime']).split('T')[0]).split('-')
    tarih = tarih[0] + '-' + tarih[1] + '-' +tarih[2]
    return tarih


def spider(url, kategori):
    data = []
    try:
        r = rq.get(url)
        """f = open("merak.html", "a", encoding='utf-8')
        f.write(str(r.html))
        f.close()"""
        soup = bs(r.content,'html.parser')                                     
        all_link = set(soup.select('a[href]'))
        alt = set(soup.select('a.footer__menu--link'))
        alt2 = set(soup.select('a.link'))
        ust = set(soup.select('a.lastmin__slide'))
        res = all_link - alt - ust - alt2
        linkler = linkDuzelt(res)     
        for link in linkler: 
            try:                        
                r = rq.get(link)           
                soup = bs(r.content, "html.parser")                     
                baslik = soup.find('h1').text
                altBaslik = ''
                if soup.find('h2') is not None:
                    altBaslik = soup.find('h2').text
                content = soup.find_all('p')
                asil = altBaslik + ' '
                for met in content:
                    if met.text != '&nbsp' and 'Hurriyet.com.tr' not in met.text:               
                        asil += met.text + ' '
                data.append(['Hürriyet',link, kategori, baslik.replace('\n',''), asil.replace('\n','').replace(u'\xa0', u' '), tarihBul(soup)])         
            except Exception:
                continue

    except Exception:
        spider(url, kategori)
    header = ['site','link', 'kategori', 'başlık', 'text', 'tarih']
    filename = 'Haberler.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerows(data) # 5. write the rest of the data  

sections = ["https://www.hurriyet.com.tr/dunya", "https://www.hurriyet.com.tr/magazin-haberleri", 
"https://www.hurriyet.com.tr/ekonomi","https://www.hurriyet.com.tr/kitap-sanat",
"https://www.hurriyet.com.tr/egitim","https://www.hurriyet.com.tr/sporarena",
"https://www.hurriyet.com.tr/sporarena/futbol", "https://www.hurriyet.com.tr/sporarena/basketbol","https://www.hurriyet.com.tr/gundem",
"https://www.hurriyet.com.tr/otomobil"]

kategori = ['Dünya', 'Magazin','Ekonomi','Kültür-Sanat','Eğitim','Spor','Futbol','Basketbol', 'Gündem', 'Otomobil']
def Hurriyet():
    i = 0
    for section in sections:
        spider(section, kategori[i])
        i += 1 
