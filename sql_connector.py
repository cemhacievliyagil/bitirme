import mysql.connector
import csv
from delete_duplicate import delete_duplicate
import deneme
from numpy import unicode_
import os
import pandas as pd

def dbyeYaz():
    news_keys = 'Haberler.csv'
    cnx = mysql.connector.connect(
        user='root',
        password='',
        database='mysql')
    """if cnx.is_connected():
                print('Connected to MySQL database')
    else:
        print("bağlanamadı..")"""
    cursor = cnx.cursor()
    with open(news_keys, mode='r', encoding="utf-8") as csv_data:
        reader = csv.reader(csv_data, delimiter=',')
        csv_data_list = list(reader)
        for row in csv_data_list:
            cursor.execute("""
                    INSERT INTO news_keys(
                    site, link, kategori, baslik, tarih)
                    VALUES(%s,%s,%s,%s,%s)""",
                        (row[0], row[1], row[2], row[3],row[5]))
            #print("EKLENDİ")
    cnx.commit()
    cursor.close()
    cnx.close()
    delete_duplicate()
    deleteSameLink()
    #print("Done")
    
def keyEkle():
    news_keys = 'Haberler.csv'
    cnx = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='mysql')

    cursor = cnx.cursor()
    with open(news_keys, mode='r', encoding="utf-8") as csv_data:
        csv_data.seek(0)
        reader = csv.reader(csv_data, delimiter=',')
        csv_data_list = list(reader)
        for row in csv_data_list:
            with open('news.txt',"w+", encoding='utf-8') as text_file:
                text_file.write(row[4])
                text_file.seek(0)
                metin = text_file.read()
                result = deneme.funct(metin)
                sql = """ UPDATE news_keys SET key1=%s, key2=%s, key3=%s, key4=%s, key5=%s, key6=%s, key7=%s, key8=%s WHERE link = %s """
                val = (result[0], result[1], result[2], result[3],result[4],result[5], result[6], result[7], row[1])
                f = open('news.txt', 'r+')
                f.truncate(0)
                f.close()
                #print("KEYWORDLER")
            cursor.execute(sql,val)
            cnx.commit()    
            #print(result)
    becameEx()

def deleteSameLink():  
    file_name = "Haberler.csv"
    df = pd.read_csv(file_name, sep=",", encoding='utf-8', header=None)
    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=[1], inplace = True)

    # Write the results to a different file
    df.to_csv(file_name, index=False, header=None)



def becameEx():
    f=pd.read_csv("Haberler.csv", header=None)
    new_f = f[1]
    new_f.to_csv("ExHaberler.csv", mode='a', header=False, index=False)
    f = open("Haberler.csv", "w+")
    f.close()
