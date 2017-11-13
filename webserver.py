#!/usr/bin/env python
import cgi
import cgitb
import socket
import sys

cgitb.enable()
print("Content-Type: text/html;charset=uft-8\r\n\r\n")

#pega os dados que o cliente informou no formulario
dadosFormulario = cgi.FieldStorage()
print dadosFormulario

#cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#address = ('192.168.56.101')

