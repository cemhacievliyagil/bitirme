from asyncio.windows_events import NULL
from multiprocessing import Value
from datetime import datetime,timedelta
from optparse import Values
from tkinter import Variable
from unittest import result
from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
import mysql.connector
from news_page import calculate_it
from kisaltma import kisaltmalar
from tarihal import tarihal
app=Flask(__name__,template_folder='templates')
Bootstrap(app)
first_name = ""
@app.route('/')
def my_form():
    return render_template('web.html')
@app.route('/', methods =["GET","POST"])
def my_form_post():
    num = request.form['a']
    kategoriler = ['Gündem', 'Siyaset','Ekonomi','Dünya','Magazin','Otomobil','Teknoloji','Eğitim','Spor','Futbol','Basketbol', 'Kültür-Sanat', 'Yaşam', 'Sağlık', 'Bilim']
    goster= 0
    print(num)
    numInt = num
    numInt1 = ""
    kisaltma = kisaltmalar()
    for x in kisaltma:
        if (numInt.upper() == x[0]):
            numInt= x[1]
    print(numInt)
    
    b = (datetime.now().strftime('%d-%m-%Y'))
    bugun = str(b)
    d = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')
    dun = str(d)


    cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
    cursor = cnx.cursor()

    if (numInt.capitalize() in kategoriler):
        cursor.execute("SELECT * FROM news_keys WHERE kategori = %s ", (numInt,))
        data = sorted(cursor.fetchall(),key=lambda x: x[5],reverse=True)
        goster = 1
        try:
         result = calculate_it(numInt.lower())
        except KeyError:
         result = [""]
    else:
     cursor.execute("SELECT * FROM news_keys WHERE key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s OR key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s",(numInt,numInt,numInt,numInt,numInt,numInt.title(),numInt.title(),numInt.title(),numInt.title(),numInt.title()))
     res=cursor.fetchall()
     if(len(res) == 0):
       data = [["","","","","Bulunamadı!"]]
       result = [""]
       goster = 0
     else:
      cursor.execute("SELECT * FROM news_keys WHERE key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s OR key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s",(numInt,numInt,numInt,numInt,numInt,numInt.title(),numInt.title(),numInt.title(),numInt.title(),numInt.title()))
      goster = 1
      data = sorted(cursor.fetchall(),key=lambda x: x[5],reverse=True)
      try:
       result = calculate_it(numInt.lower())
      except KeyError:
       result = ["Bulunamadı!"]
    return render_template('result.html',data = data, Variable= result,show = goster,bugun = bugun,dun = dun)









@app.route('/update', methods =["POST","GET"])
def onerilen_ara():
    kategoriler = ['Gündem', 'Siyaset','Ekonomi','Dünya','Magazin','Otomobil','Teknoloji','Eğitim','Spor','Futbol','Basketbol', 'Kültür-Sanat', 'Yaşam', 'Sağlık', 'Bilim']
    goster= 0
    num = request.form['b']
    numInt = num
    numInt1 = ""
    kisaltma = kisaltmalar()
    for x in kisaltma:
        if (numInt.upper() == x[0]):
            numInt= x[1]
    
    b = (datetime.now().strftime('%d-%m-%Y'))
    bugun = str(b)
    d = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')
    dun = str(d)

    print(numInt)
    cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
    cursor = cnx.cursor()

    if (numInt.capitalize() in kategoriler):
        cursor.execute("SELECT * FROM news_keys WHERE kategori = %s ", (numInt,))
        data = cursor.fetchall()
        goster = 1
        try:
         result = calculate_it(numInt.lower())
        except KeyError:
         result = [""]
    else:
     cursor.execute("SELECT * FROM news_keys WHERE key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s OR key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s",(numInt,numInt,numInt,numInt,numInt,numInt.title(),numInt.title(),numInt.title(),numInt.title(),numInt.title()))
     res=cursor.fetchall()
     if(len(res) == 0):
       data = [["","","","","Bulunamadı!"]]
       result = [""]
       goster = 0
     else:
      cursor.execute("SELECT * FROM news_keys WHERE key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s OR key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s",(numInt,numInt,numInt,numInt,numInt,numInt.title(),numInt.title(),numInt.title(),numInt.title(),numInt.title()))
      goster = 1
      data = cursor.fetchall()

      
      try:
       result = calculate_it(numInt)
      except KeyError:
       result = ["Bulunamadı!"]
    return render_template('result2.html',data = data, Variable= result,show = goster,bugun = bugun,dun = dun)











@app.route('/update-1', methods =["GET","POST"])
def dates_news():
    num = request.form['date']
    goster= 0
    numInt1 = ""
    try:
        numInt = str(datetime.strptime(num, "%Y-%m-%d").strftime("%d-%m-%Y"))
    except ValueError:
        numInt = ""
    print(numInt)
    b = (datetime.now().strftime('%d-%m-%Y'))
    bugun = str(b)
    d = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')
    dun = str(d)


    cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
    cursor = cnx.cursor()

    
    
    cursor.execute("SELECT * FROM news_keys WHERE tarih = %s",(numInt,))
    res=cursor.fetchall()
    if(len(res) == 0):
       data = [["","","","","Bulunamadı!"]]
       result = [""]
       goster = 0
    else:
      cursor.execute("SELECT * FROM news_keys WHERE tarih = %s",(numInt,))
      goster = 1
      data = sorted(cursor.fetchall(),key=lambda x: x[5],reverse=True)
      try:
       result = calculate_it(numInt.lower())
      except KeyError:
       result = ["Bulunamadı!"]
    return render_template('result3.html',data = data,show = goster,bugun = bugun,dun = dun)


if __name__ == "__main__":
    app.run()
