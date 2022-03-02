import datetime
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
    for a in res: 
        a = a.find_all('a')      
        for link in a: 
            if not link.has_attr('data-newsname'):
                continue
            href = link['href']
            if href is None or href == '':   
                continue      
            if '/yazarlar/' not in href and '/video/' not in href and '/galeri/' not in href and '/hteditor/' not in href and '/mac-detay/' not in href and '/htgastro/' not in href:
                if '.com' not in href:                 
                    linkler.append('https://www.haberturk.com'+href)
                    #print('https://www.haberturk.com'+link['href'])
                elif 'www.haberturk' in  href:
                    linkler.append(href)
                #print(link['href'])
                                                       
    linkler = list(dict.fromkeys(linkler))
    return linkler


def tarihBul(soup):   
    tarih = soup.find('time')  
    tarih = tarih.text.split()[0].replace('.', '-')
    tarih = str(datetime.datetime.strptime(tarih, "%d-%m-%Y").strftime("%Y-%m-%d"))
    return tarih


def spider(url, kategori):
    data = []
    dizi = ['last-minute-area', 'box-background box-news', 'item color-white', 'box column-12 type2', 'swiper-pagination pagination swiper-pagination-bullets', 
    'bbcWidgetIn', 'type-4', 'swiper-slide slide-item', 'wrapper', 'middleBigNewsContent', 'box column-12 type3', 'owl-page', 'swiper-slide color-yellow']
    try:
        r = rq.get(url)
        """f = open("merak.html", "a", encoding='utf-8')
        f.write(str(r.html))
        f.close()"""
        soup = bs(r.content,'html.parser')                                     
        all_link = soup.find_all("div", {'class': dizi})    
        linkler = linkDuzelt(all_link)  
        """print(kategori)
        print ("\n".join(linkler))"""
        for link in linkler:   
            try:                      
                r = rq.get(link)           
                soup = bs(r.content, "html.parser")                              
                baslik = soup.find('h1').text.strip()
                altBaslik = ''
                if soup.find('h2') is not None:
                    altBaslik = soup.find('h2').text.strip()
                content = soup.find('article',attrs={"class":["content type1","content type1 photo-section"]}).find_all('p')
                asil = altBaslik + ' '
                for met in content:
                    if met.find('div'):
                        continue
                    text = met.text.strip()
                    if text != '' and text != '&nbsp':               
                        asil += text + ' '
                data.append(['Habertürk',link, kategori, baslik.replace('\n',''), asil.replace('\n','').replace(u'\xa0', u' '), tarihBul(soup)])        
            except Exception:
                continue

    except Exception:
        spider(url, kategori)
    header = ['site','link', 'kategori', 'başlık', 'text', 'tarih']
    filename = 'Haberler.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerows(data) # 5. write the rest of the data  

sections = ["https://www.haberturk.com/saglik", "https://www.haberturk.com/ekonomi","https://www.haberturk.com/dunya","https://www.haberturk.com/magazin",
"https://www.haberturk.com/ekonomi/teknoloji","https://www.haberturk.com/spor","https://www.haberturk.com/gundem",
"https://www.haberturk.com/gundem/politika", "https://www.haberturk.com/ekonomi/otomobil", "https://www.haberturk.com/spor/futbol","https://www.haberturk.com/spor/basketbol"]

kategori = ['Sağlık','Ekonomi','Dünya','Magazin','Teknoloji','Spor','Gündem','Siyaset', 'Otomobil', 'Futbol', 'Basketbol']
def Haberturk():
    i = 0
    for section in sections:
        spider(section, kategori[i])
        i += 1 
