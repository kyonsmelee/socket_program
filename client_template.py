#-*- coding:utf-8 -*-
import socket

host = '****'
port =  ****

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

with open('file_name.***','r') as f:
    data = f.read()

client.send(data)

