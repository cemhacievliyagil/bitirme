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
    for att in res:
        if att.has_attr('onclick'):
            linkler.append(att['href'])
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
        res = soup.find_all('a', class_='content-timeline__link clearfix')        
        linkler = linkDuzelt(res)      
        for link in linkler:   
            try:                      
                r = rq.get(link)           
                soup = bs(r.content, "html.parser") 
                        
                baslik = soup.find('h1').text
                altBaslik = soup.find('div', class_='content-body__description').text
                content = soup.find('div', class_='content-body__detail')
                asil = altBaslik + ' '
                for tag in content:               
                    if tag.name == 'p' or tag.name == 'h2':
                        asil += tag.text + ' '
                    elif tag.name == 'ul' or tag.name == 'ol':
                        for li in tag:
                            asil += li.text + ' '
                data.append(['Webtekno',link, kategori, baslik.replace('\n',''), asil.replace('\n','').replace(u'\xa0', u' '), tarihBul(soup)])           
            except Exception:
                continue

    except Exception:
        spider(url, kategori)
    header = ['site','link', 'kategori', 'başlık', 'text', 'tarih']
    filename = 'Haberler.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerows(data) # 5. write the rest of the data  

sections = ["https://www.webtekno.com/yazilim", "https://www.webtekno.com/bilim-haberleri", 
"https://www.webtekno.com/donanim","https://www.webtekno.com/egitim","https://www.webtekno.com/giyilebilirteknoloji",
"https://www.webtekno.com/internet","https://www.webtekno.com/kripto-para","https://www.webtekno.com/mobil",
"https://www.webtekno.com/mobil-uygulama", "https://www.webtekno.com/otomobil", "https://www.webtekno.com/oyun","https://www.webtekno.com/sektorel"
,"https://www.webtekno.com/sinema", "https://www.webtekno.com/sosyal-medya", "https://www.webtekno.com/uzay","https://www.webtekno.com/yapay-zeka","https://www.webtekno.com/yasam"]


kategori = ['Teknoloji', 'Bilim','Teknoloji','Eğitim','Teknoloji','Teknoloji','Ekonomi','Teknoloji','Teknoloji', 'Otomobil', 
'Teknoloji', 'Ekonomi', 'Kültür-Sanat', 'Teknoloji', 'Bilim', 'Teknoloji', 'Yaşam']
def Webtekno():
    i = 0
    for section in sections:
        spider(section+'?filter_type=news', kategori[i])
        i += 1 
