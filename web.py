from asyncio.windows_events import NULL
from multiprocessing import Value
from datetime import datetime,timedelta
from optparse import Values
from tkinter import Variable
from unittest import result
from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
import mysql.connector
from numpy import hamming
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
        data = list(map(list,data))
        for y in data:
          y[5] = tarihal(str(y[5]))
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
      data = list(map(list,data))
      for y in data:
        y[5] = tarihal(str(y[5]))
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

    cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
    cursor = cnx.cursor()

    if (numInt.capitalize() in kategoriler):
        cursor.execute("SELECT * FROM news_keys WHERE kategori = %s ", (numInt,))
        data = sorted(cursor.fetchall(),key=lambda x: x[5],reverse=True)
        print(data)
        data = list(map(list,data))
        for y in data:
          y[5] = tarihal(str(y[5]))
          
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
      print(data)
      data = list(map(list,data))
      for y in data:
          y[5] = tarihal(str(y[5]))
          
      try:
       result = calculate_it(numInt)
      except KeyError:
       result = ["Bulunamadı!"]
    return render_template('result2.html',data = data, Variable= result,show = goster,bugun = bugun,dun = dun)











@app.route('/update-1', methods =["GET","POST"])
def dates_news():
    num = request.form['date']
    numInt = num
    goster= 0
    numInt1 = ""
    #try:
        #numInt = str(datetime.strptime(num, "%Y-%m-%d").strftime("%d-%m-%Y"))
    #except ValueError:
     #   numInt = ""
    #print(numInt)
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
      data = list(map(list,data))
      for y in data:
        y[5] = tarihal(str(y[5]))
      try:
       result = calculate_it(numInt.lower())
      except KeyError:
       result = ["Bulunamadı!"]
    return render_template('result3.html',data = data,show = goster,bugun = bugun,dun = dun)



@app.route('/rapor', methods =["GET","POST"])
def rapor():
    num = request.form['rapor']


    cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
    cursor = cnx.cursor()

    
    
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Sözcü" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res1=cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Hürriyet" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res2 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Milliyet" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res3 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Habertürk" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res4 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Posta" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res5 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Webtekno" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res6 = cursor.fetchall()
    cursor.execute("""SELECT site as Haber_Kaynağı, COUNT(*) AS Haber_Miktarı FROM news_keys WHERE tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) GROUP BY site ORDER by Haber_Miktarı DESC;""")
    res7 = cursor.fetchall()
    return render_template('rapor.html',res1 = res1,res2 = res2,res3 = res3,res4 = res4,res5 = res5,res6 = res6,res7=res7)




@app.route('/rapor1', methods =["GET","POST"])
def rapor1():
    #num = request.form['rapor1']


    cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
    cursor = cnx.cursor()

    
    
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Sözcü" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res1=cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Hürriyet" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res2 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Milliyet" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res3 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Habertürk" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res4 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Posta" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res5 = cursor.fetchall()
    cursor.execute("""SELECT kategori AS Kategori, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE site="Webtekno" AND tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY kategori ORDER by Haber_Sayısı DESC;""")
    res6 = cursor.fetchall()
    cursor.execute("""SELECT site as Haber_Kaynağı, COUNT(*) AS Haber_Miktarı FROM news_keys WHERE tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) GROUP BY site ORDER by Haber_Miktarı DESC;""")
    res7 = cursor.fetchall()
    return render_template('rapor1.html',res1 = res1,res2 = res2,res3 = res3,res4 = res4,res5 = res5,res6 = res6,res7=res7)

@app.route('/rapor2', methods =["GET","POST"])
def rapor2():
    return render_template('rapor2.html')

@app.route('/rapor3', methods =["GET","POST"])
def rapor3():
  kisaltma = kisaltmalar()
  haftalik = 1
  aylik=1
  num = request.form['a']
  numInt = num
  for x in kisaltma:
        if (numInt.upper() == x[0]):
            numInt= x[1]
  cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='mysql')
  cursor = cnx.cursor()
  cursor.execute("""SELECT site, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE (key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s OR key6 = %s OR key7 = %s OR key8 = %s) and tarih >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 	GROUP BY site ORDER by Haber_Sayısı DESC;""",(numInt,numInt,numInt,numInt,numInt,numInt,numInt,numInt))
  res1=cursor.fetchall()
  if(len(res1) == 0):
    res1 = "Bulunamadı"
    haftalik =0
  cursor.execute("""SELECT site, COUNT(link) AS Haber_Sayısı FROM news_keys WHERE (key1 = %s OR key2 = %s OR key3 = %s OR key4 = %s OR key5 = %s OR key6 = %s OR key7 = %s OR key8 = %s) and tarih >= DATE_ADD(CURDATE(), INTERVAL -30 DAY) 	GROUP BY site ORDER by Haber_Sayısı DESC;""",(numInt,numInt,numInt,numInt,numInt,numInt,numInt,numInt))
  res2 = cursor.fetchall()
  if(len(res2) == 0):
    res2 = "Bulunamadı"
    aylik =0
  numInt = numInt.capitalize()
  return render_template('rapor3.html',res1 = res1, res2=res2,numInt = numInt,haftalik=haftalik, aylik=aylik)



if __name__ == "__main__":
    app.run()
