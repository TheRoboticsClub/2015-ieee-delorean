#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import serial
import fcntl
import struct


# ser = serial
ser = serial.Serial('/dev/ttyUSB0', 9600)

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def get_ip(ifname):
    ip = socket.inet_ntoa(fcntl.ioctl(mySocket.fileno(), 
         0x8915, struct.pack('256s', ifname[:15]))[20:24])
    return ip

public_ip = str(get_ip('eth0'))
print public_ip
mySocket.bind((public_ip, 1234))
mySocket.listen(5)

try:
    while True:
        print "Waiting for connections..."
        (recvSocket, address) = mySocket.accept()
        print "HTTP request received"
        peticion = recvSocket.recv(1024)
        print peticion
        comando = peticion.split()[1][1:]
        print "Answring back..."
        recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" + 
                        "<html><body><h1>Mu bien</h1></body></html>" +
                        "\r\n")
        ser.write(comando)
        recvSocket.close()
except KeyboardInterrupt:
    print "Stopping server"
    mySocket.close()
