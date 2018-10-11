#-*- coding:utf-8 -*-
import socket

host = '****'
port =  ****

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #IPとportを指定してbind
serversock.listen(10) #接続の待ち受け

print 'Waiting for connections...'

while True:
    clientsock,client_address = serversock.accept() #接続されればデータを格納
    data = clientsock.recv(1024*1024)
        
    with open('filename.***', 'w') as f:
        f.write(data)
            
        if data=='':
            break
