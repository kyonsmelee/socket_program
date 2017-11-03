#-*- coding:utf-8 -*-
import socket
import time

host = '192.168.100.70'
port = 8000

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #IPとportを指定してbind
serversock.listen(10) #接続の待ち受け

print 'Waiting for connections...'
count = 0

while True:
    clientsock,client_address = serversock.accept() #接続されればデータを格納

    time.sleep(0.1)
    data = clientsock.recv(1024*1024)
    print data

    with open("/Users/kyonsu/Desktop/rssi_data/rssi_docomo_"+ str(count) +".csv", "wb") as f:
        f.write(data)

    if data=='':
        break

    count += 1
    print "get data"

