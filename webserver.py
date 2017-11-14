#!/usr/bin/env python
import cgi
import cgitb
import socket
import sys
import binascii

cgitb.enable()
print("Content-Type: text/html;charset=uft-8\r\n\r\n")

#pega os dados que o cliente informou no formulario
dadosFormulario = cgi.FieldStorage()

#informacoes dos daemons
hostDaemons = "127.0.0.1"
portaDaemon1 = 9006
portaDaemon2 = 9002
portaDaemon3 = 9003

#TODO: pegar dados do formulario
#TODO: fazer pros outros daemons

def encaminhaPacote():
	#cria o socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#faz a conexao com o daemon
	s.connect((hostDaemons, portaDaemon1))

	try:
		#envia os dados
		msg = criaMensagem()
		s.sendall(msg)
		
		#fica esperando a resposta
		dados = s.recv(4096)
		
		#printa o resultado na tela
		resultado = dados[160:]
		print "Machine #1<br>"
		resultado = resultado.replace("\n","<br>")
		print resultado
	finally:
		s.close()

def criaMensagem():
	#TODO: protocolo
	msg = "0010" #version=2 (4 bits)
	msg += "1111"#ihl(4 bits)
	msg += "00000000" #type of service (8 bits)
	msg += "0000000000000000" #total length (16 bits)
	msg += "0000000000000000" #identification (16 bits)
	msg += "000" #flags= 000 (requisicao) (3 bits)
	msg += "0000000000000" # fragment offset = 0 (13 bits)
	msg += "11111111" #time to live = 255 (8 bits)
	msg += "00000001" #protocol =ps (8 bits)
	msg += "0101010101010101"#header checksum (16bits)
	msg += "11000000"+"10101000"+"00111000"+"01100101" #source address=192.168.56.101 (32 bits)
	msg+= "01111111"+"00000000"+"00000000"+"00000001" #destination addres=127.0.0.1
	msg+=bin(int(binascii.hexlify('-ef'),16))#options
	return msg[0:16]+ bin(len(msg))[2:].zfill(16)+ msg[32:len(msg)]


#TODO: criar as threads
encaminhaPacote()
