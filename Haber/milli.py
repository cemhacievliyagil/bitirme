import datetime
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
        if link['href'][-1].isnumeric() and '/yazarlar/' not in link['href'] and '.apple' not in link['href'] and '/pembenar/' not in link['href']: 
            if 'aspx?' not in link['href'] and '/skorer-tv/' not in link['href']:
                rakam = link['href'].split("-")[-1]                    
                linkler.append('https://www.milliyet.com.tr/'+rakam)
                                                       
    linkler = list(dict.fromkeys(linkler))
    return linkler


def tarihBul(soup,link):
    tarih = ''   
    if soup.find('span', class_ = 'rhd-time-box-text rgc_date') is not None:
        tarih = soup.find('span', class_ = 'rhd-time-box-text rgc_date').text.split()
        tarih = tarih[3] + '-' + aylar[tarih[2]] + '-' + tarih[1]
    else:
        tarih = soup.find('div', class_ = 'nd-article__info-block').text.split()
        tarih = tarih[0].replace('.', '-')
        tarih = str(datetime.datetime.strptime(tarih, "%d-%m-%Y").strftime("%Y-%m-%d"))
    return tarih


def spider(url, kategori):
    data = []
    try:
        page = rq.get(url)  
        """f = open("merak.html", "a", encoding='utf-8')
        f.write(str(page))
        f.close() """               
        soup = bs(page.content, "html.parser")               
        all_link = set(soup.select('a'))
        X = set(soup.select('a.gf-group__link'))
        Y = set(soup.select('a.category-links__list-item'))                
        res = all_link - X - Y 
        linkler = linkDuzelt(res)       
        for link in linkler:  
            try:                       
                page = rq.get(link)                
                soup = bs(page.content, "html.parser")
                if soup.find('div', class_ ='article__author__wrapper') is not None:
                    continue
                baslik = soup.find('h1').text
                altBaslik = ''
                if soup.find('h2') is not None:
                    altBaslik = soup.find('h2').text
                metin = soup.find_all('p', title = False)
                asil = altBaslik
                metinGaleri = soup.find_all('h3', class_ = 'description')
                asilGaleri = altBaslik
                for met in metinGaleri:
                    asilGaleri = asilGaleri + ' ' + met.text
                for met in metin:
                    asil = asil + ' ' + met.text                      
                data.append(['Milliyet',link, kategori, baslik, asil, tarihBul(soup,link)])
            except Exception:
                continue

    except Exception:
        spider(url, kategori)
    header = ['site','link', 'kategori', 'başlık', 'text', 'tarih']
    filename = 'Haberler.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerows(data) # 5. write the rest of the data  

sections = ["https://www.milliyet.com.tr/gundem", "https://www.milliyet.com.tr/siyaset", "https://www.milliyet.com.tr/ekonomi", "https://www.milliyet.com.tr/dunya",
"https://www.milliyet.com.tr/magazin", "https://www.milliyet.com.tr/otomobil", "https://www.milliyet.com.tr/teknoloji", "https://www.milliyet.com.tr/egitim",
"https://www.milliyet.com.tr/skorer", "https://www.milliyet.com.tr/skorer/futbol-haberleri",
"https://www.milliyet.com.tr/skorer/basketbol-haberleri", "https://www.milliyet.com.tr/kultur-sanat", "https://www.sozcu.com.tr/hayatim/yasam-haberleri"]

kategori = ['Gündem', 'Siyaset','Ekonomi','Dünya','Magazin','Otomobil','Teknoloji','Eğitim','Spor','Futbol','Basketbol', 'Kültür-Sanat', 'Yaşam']
def Milliyet():
    i = 0
    for section in sections:
        spider(section, kategori[i])
        i += 1 
