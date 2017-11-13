#!/usr/bin/env python
import cgitb
import socket
import sys

cgitb.enable()

#cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#liga o socket com o host e a porta
s.bind(("127.0.0.1",9001))

#deixa o socket na espera de possiveis conexoes
s.listen(1)

while True:
	print "[Daemon 1] Esperando conexao..."
	conexao, endCliente = s.accept()

	try:
		print >>sys.stderr, "[Daemon 1] Conexao com o cliente: ", endCliente
		while True:
			dados = conexao.recv(4096)
			print >>sys.stderr, "[Daemon1] Dados recebidos: %s " % dados
			if dados:
				print "[Daemon 1] Enviando dados de volta"
				conexao.sendall("Leticia e Stephanie")
			else:
				print "[Daemon 1] Acabou os dados."
				break
	finally:
		conexao.close()


#TODO: outros daemons!!
#TODO: executar os comandos
