#!/usr/bin/python3.9
from socket import socket, AF_INET, SOCK_STREAM

client = socket(family = AF_INET, type = SOCK_STREAM)
client.connect(('localhost', 9473))

while True:
    message = input('Type your message: ')
    if not message:
        break
    client.send(message.encode())
socket.close()