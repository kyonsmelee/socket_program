#-*- coding:utf8 -*-

import socket
import threading
import time
import os
import colorama
from colorama import Fore,Back,Style
import datetime
import sys
import time

def docomo_thread():
    host = '192.168.100.105'
    port = 8003

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け

    print 'Waiting Docomo client for connections...'
    clientsock,client_address = serversock.accept() #接続されればデータを格納

    while True:
        time.sleep(0.1)
        data = clientsock.recv(1024*1024)
        with open("/data/shibata/server/server_data/data_docomo.zip", "a") as f:
            f.write(data)
            if data=='':
                os.system("unzip /data/shibata/server/server_data/data_docomo.zip -d /data/shibata/server/server_data/rssi_data_docomo")
                os.system("rm /data/shibata/server/server_data/data_docomo.zip")
                break

    now = datetime.datetime.now()

    os.system("cp -v /data/shibata/server/server_data/rssi_data_docomo/data_docomo.csv /data/shibata/server/server_data/rssi_data_docomo/data_docomo_{0:%Y%m%d%H%M%S}.csv".format(now))
    os.system("mv /data/shibata/server/server_data/rssi_data_docomo/data_docomo.csv /data/shibata/server/server_data/ana_data/data_docomo_log.csv")

    print "Docomo server get data!"

def au_thread():
    host = '192.168.100.105'
    port = 8004

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け

    print 'Waiting au client for connections...'
    clientsock,client_address = serversock.accept() #接続されればデータを格納

    while True:
        time.sleep(0.1)
        data = clientsock.recv(1024*1024)

        with open("/data/shibata/server/server_data/data_au.zip", "a") as f:
            f.write(data)

        if data=='':
            os.system("unzip /data/shibata/server/server_data/data_au.zip -d /data/shibata/server/server_data/rssi_data_au")
            os.system("rm /data/shibata/server/server_data/data_au.zip")
            break

    now = datetime.datetime.now()

    os.system("cp -v /data/shibata/server/server_data/rssi_data_au/data_au.csv /data/shibata/server/server_data/rssi_data_au/data_au_{0:%Y%m%d%H%M%S}.csv".format(now))
    os.system("mv /data/shibata/server/server_data/rssi_data_au/data_au.csv /data/shibata/server/server_data/ana_data/data_au_log.csv")

    print "au server get data!"

def softbank_thread():
    host = '192.168.100.105'
    port = 8005

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け

    print 'Waiting SoftBank client for connections...'
    clientsock,client_address = serversock.accept() #接続されればデータを格納

    while True:
        time.sleep(0.1)
        data = clientsock.recv(1024*1024)

        with open("/data/shibata/server/server_data/data_softbank.zip", "a") as f:
            f.write(data)

        if data=='':
            os.system("unzip /data/shibata/server/server_data/data_softbank.zip -d /data/shibata/server/server_data/rssi_data_softbank")
            os.system("rm /data/shibata/server/server_data/data_softbank.zip")
            break

    now = datetime.datetime.now()

    os.system("cp -v /data/shibata/server/server_data/rssi_data_softbank/data_softbank.csv /data/shibata/server/server_data/rssi_data_softbank/data_softbank_{0:%Y%m%d%H%M%S}.csv".format(now))
    os.system("mv /data/shibata/server/server_data/rssi_data_softbank/data_softbank.csv /data/shibata/server/server_data/ana_data/data_softbank_log.csv")

    print "SoftBank server get data!"

def analysis_thread():
    print "\n"
    print "get all data!!"
    print "-------------"
    print "解析中"
    for i in range(10):
        print "*",
        time.sleep(1)
        if i ==9:
            print "*"
    print "解析終了"
    print "--------------"
    os.system("rm /data/shibata/server/server_data/ana_data/*.csv")
    print "解析データを削除しました。"
    print "\n"

while True:
    thread_docomo = threading.Thread(target=docomo_thread)
    thread_softbank = threading.Thread(target=softbank_thread)
    thread_au = threading.Thread(target=au_thread)

    thread_docomo.start()
    thread_softbank.start()
    thread_au.start()

    thread_docomo.join()
    thread_softbank.join()
    thread_au.join()

    thread_analysis = threading.Thread(target=analysis_thread)
    thread_analysis.start()
    thread_analysis.join()

'''
t1=time.time()
docomo_thread()
softbank_thread()
au_thread()
t2 = time.time()
elapsed_time = t2-t1
print "経過時間：{}".format(elapsed_time)
'''
