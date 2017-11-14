#!/usr/bin/env python
import cgitb
import socket
import sys
import binascii
import commands

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

	
#cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#liga o socket com o host e a porta
s.bind(("127.0.0.1",9006))

#deixa o socket na espera de possiveis conexoes
s.listen(1)

while True:
	print "[Daemon 1] Esperando conexao..."
	conexao, endCliente = s.accept()

	try:
		print >>sys.stderr, "[Daemon 1] Conexao com o cliente: ", endCliente
		dados = conexao.recv(4096)
		print >>sys.stderr, "[Daemon1] Dados recebidos: %s " % dados
		msg = executaComando(dados)
		if dados:
			print "[Daemon 1] Enviando dados de volta"
			conexao.sendall(msg)
		else:
			print "[Daemon 1] Acabou os dados."
			break
	finally:
		conexao.close()


#TODO: outros daemons!!
