#!/usr/bin/python3.9
from socket import socket, AF_INET, SOCK_STREAM

server = socket(family = AF_INET, type = SOCK_STREAM)

server.bind(('localhost', 9473))
server.listen()

conn, addr = server.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break
   
    print('New message from host %s:\n%s' %(addr, data.decode()))
conn.close()