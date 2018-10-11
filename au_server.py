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
port_gps = 8004
port_au = 8005
count_au = 1

serversock_gps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock_gps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock_gps.bind((host,port_gps)) #IPとportを指定してbind
serversock_gps.listen(10) #接続の待ち受け

serversock_au = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock_au.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock_au.bind((host,port_au)) #IPとportを指定してbind
serversock_au.listen(10) #接続の待ち受け

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
    print 'Waiting for au client...'
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

    while True:
        clientsock_au,client_address = serversock_au.accept() #接続されればデータを格納
        start = time.time()
        while True:
            au_data = clientsock_au.recv(1024*1024) #クライアントからのデータを受信
            
            with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.zip", 'a') as f:
                f.write(au_data) #受信データをファイルに書き出し
                if au_data=='':
                    elapsed_time = time.time() - start
                    os.system("unzip /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.zip -d /Users/kyonsu/Desktop/研究/socket/rssi_data_au")
                    with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au_time.csv",'a') as f1:
                        f1.write(str(elapsed_time))
                        f1.write("\nr")
                    print elapsed_time
                    break #受信データが無くなれば終了
        break

    os.system("cp -f /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au_" + str(count_au) + ".csv") #受信データを書き出したファイルを別ファイルにコピー
    os.system("mv -f /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au_log.csv") #コピー元ファイルの名前を変更し解析プログラムで使用
    print Fore.RED + "au server" +  Fore.WHITE + " get data!"
    #os.system("python /Users/kyonsu/Desktop/研究/Tensorflow/DNN_Evaluation_au.py 3000 70 30 21 0.8")
    os.system("rm /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.zip")

    '''
    cur = conn.cursor() #Cursorオブジェクトを作成してexecute()メソッドを呼び出してSQL文を実行する
    insert_sql ='UPDATE Cafeteria SET lat={},lng={} WHERE career="au"'.format(data_split[0],data_split[1])
    cur.execute(insert_sql)
    conn.commit() #クエリ実行時にコミットする
    '''
    count_au += 1


