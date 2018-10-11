#-*- coding:utf-8 -*-

from urlparse import urlparse
import mysql.connector

url = urlparse('mysql://kyons:kyons@localhost:3306/PeopleCount')

'''
conn = mysql.connector.connect(
                               host = url.hostname or 'localhost',
                               port = url.port or 3306,
                               user = url.username or 'root',
                               password = url.password or '',
                               database = url.path[1:],
)
'''

conn = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = url.username,
    password = url.password,
    database = url.path[1:],
)

conn.ping(reconnect=True) #コネクションが切断していれば再接続する

list_gps = ["10.0","20.0"]
insert_sql = 'UPDATE Cafeteria SET lat={},lng={} WHERE career="docomo"'.format(list_gps[0],list_gps[1])
cur = conn.cursor() #クエリの実行
#cur.execute('SELECT * FROM Cafeteria')
cur.execute(insert_sql)
conn.commit()
#print cur.fetchall()
