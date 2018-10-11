#-*- coding:utf-8 -*-
import socket
import numpy as np
import threading
import time
import sys
import os
from colorama import Fore,Back,Style
from urlparse import urlparse
import mysql.connector

host = '192.168.100.68'
port_gps = 8002
port_docomo = 8003
count_docomo = 1

serversock_gps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock_gps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock_gps.bind((host,port_gps)) #IPとportを指定してbind
serversock_gps.listen(10) #接続の待ち受け
    
serversock_docomo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock_docomo.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock_docomo.bind((host,port_docomo)) #IPとportを指定してbind
serversock_docomo.listen(10) #接続の待ち受け

'''データベースに接続'''
url = urlparse('mysql://kyons:kyons@localhost:3306/PeopleCount')
conn = mysql.connector.connect(
                               host = 'localhost',
                               port = 3306,
                               user = url.username,
                               password = url.password,
                               database = url.path[1:],
                               )

while True:
    print 'Waiting for gps data...'
    print 'Waiting for docomo client...'
    list_gps = [ ]

    while True:
        clientsock_gps,client_address = serversock_gps.accept() #接続されればデータを格納
        while True:
            gps_data = clientsock_gps.recv(1024*1024)
            list_gps.append(gps_data)
            if gps_data=='':
                break
        print 'get gps data'
        data_split = list_gps[0].split(',') #緯度、経度の取り出し
        break
    
    clientsock_docomo,client_address = serversock_docomo.accept() #接続されればデータを格納

    '''
    while True:
        docomo_data = clientsock_docomo.recv(1024*1024) #クライアントからのデータを受信
        with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.csv", 'a') as f:
            f.write(docomo_data) #受信データをファイルに書き出し
        if docomo_data=='':
            break #受信データが無くなれば終了
    '''
    
    while True:
        docomo_data = clientsock_docomo.recv(1024*1024) #クライアントからのデータを受信
        with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.zip", 'a') as f:
            f.write(docomo_data) #受信データをファイルに書き出し
            if docomo_data=='':
                os.system("unzip /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.zip -d /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo")
                break #受信データが無くなれば終了

    os.system("cp -f /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo_" + str(count_docomo) + ".csv") #受信データを書き出したファイルを別ファイルにコピー
    os.system("mv -f /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo_log.csv") #コピー元ファイルの名前を変更し解析プログラムで使用
    print Fore.RED + "docomo server" +  Fore.WHITE + " get data!"
    #os.system("python /Users/kyonsu/Desktop/研究/Tensorflow/DNN_Evaluation_docomo.py 3000 70 30 21 0.8")
#os.system("rm /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.zip")

    cur = conn.cursor() #Cursorオブジェクトを作成してexecute()メソッドを呼び出してSQL文を実行する
    insert_sql ='UPDATE Cafeteria SET lat={},lng={} WHERE career="docomo"'.format(data_split[0],data_split[1])
    cur.execute(insert_sql)
    conn.commit() #クエリ実行時にコミットする

    count_docomo += 1


