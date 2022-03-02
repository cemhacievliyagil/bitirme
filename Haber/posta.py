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
        href = link['href']
        if href == '' or 'https:/' in href or '/yazarlar/' in href:  
            continue      
        if href[-1].isnumeric():            
            linkler.append('https://www.posta.com.tr'+href)                                                
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
        soup = bs(r.content, "html.parser")               
        all_link = set(soup.select('a[href]'))
        alt = set(soup.select('a.fixed-ratio.fixed-ratio__4x3'))       
        ust = set(soup.select('a.nav__link'))
        alt2 = set(soup.select('a.news-list__link'))
        res = all_link - alt - ust  - alt2                       
        linkler = linkDuzelt(res) 
        #print ("\n".join(linkler))   
        for link in linkler:    
            try:                     
                r = rq.get(link)               
                soup = bs(r.content, "html.parser")              
                baslik = soup.find('h1').text.strip()
                altBaslik = ''
                if soup.find('h2', class_ = 'news-detail__info__spot'):
                    altBaslik = soup.find('h2', class_ = 'news-detail__info__spot').text   
                else:
                    altBaslik = soup.find('div', class_ = 'news-detail__body__content clearfix').text                 
                metin = soup.find_all('p', class_ = False)
                asil = altBaslik.strip() 
                """f = open("merak.html", "a", encoding='utf-8')
                f.write(str(soup))
                f.close()"""                       
                for met in metin:  
                    if met.find('div'):
                        met.find('div').decompose()
                    if met.find('blockquote'):
                        met.find('blockquote').decompose()              
                    met2 = met.text.strip()                
                    if met2 == '':
                        continue
                    asil = asil + ' ' + met2                     
                data.append(['Posta',link, kategori, baslik.replace('\n', ''), asil.replace('\n', ''), tarihBul(soup)])  
            except Exception:
                continue              
    except Exception:
        spider(url, kategori)
    header = ['site','link', 'kategori', 'başlık', 'text', 'tarih']
    filename = 'Haberler.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerows(data) # 5. write the rest of the data  

sections = ["https://www.posta.com.tr/gundem/siyaset", "https://www.posta.com.tr/gundem/turkiye", 
"https://www.posta.com.tr/dunya","https://www.posta.com.tr/spor",
"https://www.posta.com.tr/ekonomi","https://www.posta.com.tr/magazin","https://www.posta.com.tr/sosyal-yasam/bilim-teknoloji",
"https://www.posta.com.tr/sosyal-yasam/kultur-sanat", "https://www.posta.com.tr/sosyal-yasam/egitim-kariyer"]

kategori = ['Siyaset', 'Gündem','Dünya','Spor','Ekonomi','Magazin','Teknoloji','Kültür-Sanat','Eğitim']

def Posta():
    i = 0
    for section in sections:
        spider(section, kategori[i])
        i += 1 
