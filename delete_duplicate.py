import mysql.connector
def delete_duplicate():
    cnx = mysql.connector.connect(
        user='root',
        password='',
        database='mysql')
    """if cnx.is_connected():
                print('Connected to MySQL database')
    else:
        print("bağlanamadı..")"""

    cursor = cnx.cursor()
    cursor.execute("""DELETE t1 FROM news_keys t1
    INNER JOIN news_keys t2 
    WHERE 
        t1.id < t2.id AND 
        t1.link = t2.link AND
        t1.kategori = t2.kategori""")
    cnx.commit()
    cursor.close()
