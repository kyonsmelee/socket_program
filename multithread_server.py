#-*- coding:utf-8 -*-
import socket
import threading
import time
import os
import colorama
from colorama import Fore,Back,Style
import datetime
import sys

count_docomo = 1
count_au = 1
count_softbank = 1

def gps_server():
    global data_split
    host = '192.168.100.68'
    port = 8005
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け
    
    while True:
        print 'Waiting for gps data...'
        list_gps = [ ]
        while True:
            clientsock,client_address = serversock.accept() #接続されればデータを格納
            while True:
                gps_data = clientsock.recv(1024*1024)
                list_gps.append(gps_data)
                if gps_data=='':
                    break
            break
        print 'get gps data'
        data_split = list_gps[0].split(',') #緯度、経度の取り出し

def docomo_server():
    global count_docomo
    host = '192.168.100.68'
    port = 8002
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け
    
    while True:
        print 'Waiting for docomo client...'
        while True:
            clientsock,client_address = serversock.accept() #接続されればデータを格納
            
            while True:
                docomo_data = clientsock.recv(1024*1024) #クライアントからのデータを受信
                with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.csv", 'a') as f:
                    f.write(docomo_data) #受信データをファイルに書き出し
                if docomo_data=='':
                    break #受信データが無くなれば終了

            break
        os.system("cp -f /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo_" + str(count) + ".csv") #受信データを書き出したファイルを別ファイルにコピー
        os.system("mv -f /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_docomo/data_docomo_log.csv") #コピー元ファイルの名前を変更し解析プログラムで使用
        print Fore.RED + "docomo server" +  Fore.WHITE + " get data!"
        os.system("python /Users/kyonsu/Desktop/研究/Tensorflow/DNN_Evaluation_docomo.py 3000 70 30 21 0.8")
                
        count_docomo += 1

def au_server():
    global count_au
    host = '192.168.100.68'
    port = 8003
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け

    while True:
        print 'Waiting for au client ...'
        while True:
            clientsock,client_address = serversock.accept() #接続されればデータを格納
            
            while True:
                au_data = clientsock.recv(1024*1024) #クライアントからのデータを受信
                with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.csv", "a") as f:
                    f.write(au_data) #受信データをファイルに書き出し
                if data=='':
                    break #受信データが無くなれば終了
    
            break
        os.system("cp -f /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au_" + str(count) + ".csv") #受信データを書き出したファイルを別ファイルにコピー
        os.system("mv -f /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_au/data_au_log.csv") #コピー元ファイルの名前を変更し解析プログラムで使用
        print Fore.RED + "au server" +  Fore.WHITE + " get data!"
        os.system("python /Users/kyonsu/Desktop/研究/Tensorflow/DNN_Evaluation_au.py 3000 60 30 21 0.8")
    
        count_au += 1

def softbank_server():
    global count_softbank
    host = '192.168.100.68'
    port = 8004
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとportを指定してbind
    serversock.listen(10) #接続の待ち受け
    
    while True:
        print 'Waiting for softbank client ...'
        while True:
            clientsock,client_address = serversock.accept() #接続されればデータを格納
            
            while True:
                softbank_data = clientsock.recv(1024*1024) #クライアントからのデータを受信
                with open("/Users/kyonsu/Desktop/研究/socket/rssi_data_softbank/data_softbank.csv", "a") as f:
                    f.write(softbank_data) #受信データをファイルに書き出し
                if data=='':
                    break #受信データが無くなれば終了
    
            break
        os.system("cp -f /Users/kyonsu/Desktop/研究/socket/rssi_data_softbank/data_softbank.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_softbank/data_softbank_" + str(count) + ".csv") #受信データを書き出したファイルを別ファイルにコピー
        os.system("mv -f /Users/kyonsu/Desktop/研究/socket/rssi_data_softbank/data_softbank.csv /Users/kyonsu/Desktop/研究/socket/rssi_data_softbank/data_softbank_log.csv") #コピー元ファイルの名前を変更し解析プログラムで使用
        print Fore.RED + "softbank server" +  Fore.WHITE + " get data!"
        os.system("python /Users/kyonsu/Desktop/研究/Tensorflow/DNN_Evaluation_softbank.py 3000 70 40 21 0.8")
        
    count_softbank += 1

if __name__ == "__main__":
    try:
        thread_gps = threading.Thread(target=gps_server)
        thread_docomo = threading.Thread(target=docomo_server)
        thread_au = threading.Thread(target=au_server)
        thread_softbank = threading.Thread(target=softbank_server)
        
        thread_gps.start()
        thread_docomo.start()
        thread_au.start()
        thread_softbank.start()

    except KeyboardInterrupt:
        sys.exit()



