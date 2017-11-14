#!/usr/bin/env python
import cgi
import cgitb
import socket
import sys
import binascii

cgitb.enable()
print("Content-Type: text/html;charset=uft-8\r\n\r\n")

#pega os dados que o cliente informou no formulario
form = cgi.FieldStorage()

#informacoes dos daemons
hostDaemons = "127.0.0.1"
portaDaemon1 = 9006
portaDaemon2 = 9002
portaDaemon3 = 9003


def encaminhaPacote(daemon, comando, parametros):
	#cria o socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#faz a conexao com o daemon
	porta = 0
	if daemon==1:
		porta = portaDaemon1
	if daemon==2:
		porta = portaDaemon2
	if daemon==3:
		porta = portaDaemon3

	s.connect((hostDaemons, porta))

	try:
		#envia os dados
		msg = criaMensagem(comando, parametros)
		s.sendall(msg)
		
		#fica esperando a resposta
		dados = s.recv(4096)
		
		#printa o resultado na tela
		print "<br><br><b>Comando:</b> %s<br>" % comando
		print "<b>Parametros:</b> %s<br><br>" % parametros
		tamanho = len(dados) - 2
		resultado = dados[160:tamanho]
		resultado = resultado.replace("\n","<br>")
		print resultado
		print "<br><br>"
		print "__________________________________"
	finally:
		s.close()

def criaMensagem(comando, parametros):
	protocolo = ""
	if comando=="ps":
		protocolo = "00000001"
	if comando=="df":
		protocolo = "00000010"
	if comando=="finger":
		protocolo = "00000011"
	if comando=="uptime":
		protocolo = "00000100"

	msg = "0010" #version=2 (4 bits)
	msg += "1111"#ihl(4 bits)
	msg += "00000000" #type of service (8 bits)
	msg += "0000000000000000" #total length (16 bits)
	msg += "0000000000000000" #identification (16 bits)
	msg += "000" #flags= 000 (requisicao) (3 bits)
	msg += "0000000000000" # fragment offset = 0 (13 bits)
	msg += "11111111" #time to live = 255 (8 bits)		
	msg += protocolo #protocol (8 bits)
	msg += "0101010101010101"#header checksum (16bits)
	msg += "11000000"+"10101000"+"00111000"+"01100101" #source address=192.168.56.101 (32 bits)
	msg+= "01111111"+"00000000"+"00000000"+"00000001" #destination addres=127.0.0.1
	msg+=bin(int(binascii.hexlify(parametros),16))#options
	return msg[0:16]+ bin(len(msg))[2:].zfill(16)+ msg[32:len(msg)]

def enviaDadosMaquina1():
	print "<center><h3>MAQUINA 1</h3></center>"
	print "<hr>"
	if form.getvalue("maq1_ps"):
		encaminhaPacote(1,"ps",form.getvalue("maq1-ps"))
	if form.getvalue("maq1_df"):
		encaminhaPacote(1,"df",form.getvalue("maq1-df"))
	if form.getvalue("maq1_finger"):
		encaminhaPacote(1,"finger",form.getvalue("maq1-finger"))
	if form.getvalue("maq1_uptime"):
		encaminhaPacote(1,"uptime",form.getvalue("maq1-uptime"))

def enviaDadosMaquina2():
	print "<h3>MAQUINA 2</h3>"
	if form.getvalue("maq2_ps"):
		encaminhaPacote(2,"ps",form.getvalue("maq2-ps"))
	if form.getvalue("maq2_df"):
		encaminhaPacote(2,"df",form.getvalue("maq2-df"))
	if form.getvalue("maq2_finger"):
		encaminhaPacote(2,"finger",form.getvalue("maq2-finger"))
	if form.getvalue("maq2_uptime"):
		encaminhaPacote(2,"uptime",form.getvalue("maq2-uptime"))

def enviaDadosMaquina3():
	print "<h3>MAQUINA 3</h3>"
	if form.getvalue("maq3_ps"):
		encaminhaPacote(3,"ps",form.getvalue("maq3-ps"))
	if form.getvalue("maq3_df"):
		encaminhaPacote (3,"df",form.getvalue("maq3-df"))
	if form.getvalue("maq3_finger"):
		encaminhaPacote(3,"finger",form.getvalue("maq3-finger"))
	if form.getvalue("maq3_uptime"):
		encaminhaPacote(3,"uptime",form.getvalue("maq3-uptime"))


#TODO: criar as threads
enviaDadosMaquina1()
