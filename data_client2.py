#-*- coding:utf-8 -*-
import socket
import time

host = '21.0.0.1'
port = 8000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

with open('/Users/kyonsu/Desktop/test_data_file/test.txt','rb') as f:
    data = f.read()

client.send(data)
print 'send data1'
