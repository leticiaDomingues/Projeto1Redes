#!/usr/bin/env python
import cgitb
import socket
import sys
import binascii
import commands
from threading import Thread

cgitb.enable()


def executaComando(msg):
	#pega o comando que o usuario quer
	protocolBin = msg[72:80]
	protocolo = ""
	
	if protocolBin=="00000001":
		protocolo = "ps"
	if protocolBin=="00000010":
		protocolo = "df"
	if protocolBin=="00000011":
		protocolo = "finger"
	if protocolBin=="00000100":
		protocolo = "uptime"	

	#pega as opcoes que o usuario digitou
	optionsBin = msg[160:]
	opcoes = binascii.unhexlify('%x' % int(optionsBin,2))
	
	#execute o comando
	comando = protocolo + " " + opcoes
	resultado = commands.getstatusoutput(comando)
	
	#monta o socket
	msg = "0010" #version=2 (4 bits)
	msg += "1111" #ihl (4 bits)
	msg += "00000000" #type of service (8 bits)
	msg += "0000000000000000" #total length (16 bits)
	msg += "0101000001010000" #identification (16 bits)
	msg += "111" #flags=111 (resposta) (3 bits)
	msg += "0000000000000" #fragment offset = 0 (13 bits)
	msg += "11111110" #time to live=254 (8 bits)
	msg += protocolBin #protocol (8bits)
	msg += "01111111" + "00000000" + "00000000" + "00000001" #source address
	msg += "11000000" + "10101000" + "00111000" + "01100101" #destination
	msg += str(resultado) #resposta

	return msg[0:16]+bin(len(msg))[2:].zfill(16)+msg[32:len(msg)]

portaDaemon1 = 9001
portaDaemon2 = 9002
portaDaemon3 = 9003

def iniciaThreadDaemon(daemon):
	#cria o socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#liga o socket com o host e a porta
	porta =0
	if daemon==1:
		porta=portaDaemon1
	if daemon==2:
		porta=portaDaemon2
	if daemon==3:
		porta=portaDaemon3
	s.bind(("127.0.0.1",porta))

	#deixa o socket na espera de possiveis conexoes
	s.listen(1)

	while True:
		print "[Daemon %i] Esperando conexao..." % daemon
		conexao, endCliente = s.accept()

		try:
			dados = conexao.recv(4096)
			print >>sys.stderr, "[Daemon %i] Dados recebidos: %s " % (daemon,dados)
			msg = executaComando(dados)
			if dados:
				print "[Daemon %i] Enviando dados de volta" % daemon
				conexao.sendall(msg)
			else:
				break
		finally:
			conexao.close()


#cria as threads
thread1 = Thread(target=iniciaThreadDaemon,args=(1,))
thread2 = Thread(target=iniciaThreadDaemon,args=(2,))
thread3 = Thread(target=iniciaThreadDaemon,args=(3,))

#da start nas threads
thread1.start()
thread2.start()
thread3.start()
