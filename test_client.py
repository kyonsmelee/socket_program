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
            
            with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_au/test_au1.csv", 'a') as f:
                f.write(au_data) #受信データをファイルに書き出し
            if au_data=='':
                elapsed_time = time.time() - start
                with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au_time.csv",'a') as f1:
                    f1.write(str(elapsed_time))
                print elapsed_time
                break #受信データが無くなれば終了
        break
            
    print Fore.RED + "au server" +  Fore.WHITE + " get data!"


