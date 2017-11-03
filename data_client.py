#-*- coding:utf-8 -*-
import socket
import time

host = '192.168.100.70'
port = 8000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

with open('/Users/kyonsu/Desktop/test_data_file/rssi_1minute.csv','rb') as f:
    data = f.read()

#client.send('6')
client.send(data)
#client.send('0')

print 'send data'
