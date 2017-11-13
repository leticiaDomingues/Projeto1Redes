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

#informacoes dos daemons
hostDaemons = "127.0.0.1"
portaDaemon1 = 9001
portaDaemon2 = 9002
portaDaemon3 = 9003

#TODO: tratar dados do formulario

#TODO: fazer pros outros daemons
def encaminhaPacote():
	#cria o socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "[Webserver] Socket do daemon 1 criado com sucesso."
	
	#faz a conexao com o daemon
	s.connect((hostDaemons, portaDaemon1))
	print "[Webserver] Conexao com o daemon 1 realizada." 

	try:
		#envia dados
		msg = "Stephanie e Leticia"
		print >>sys.stderr, "[Webserver] Enviando a msg: %s para Daemon 1" % msg
		s.sendall(msg)
	
		#loop infinito
		tamanhoEnviado = len(msg)
		tamanhoRecebido = 0

		while tamanhoRecebido < tamanhoEnviado:
			dados = s.recv(4096)
			tamanhoRecebido += len(dados)
			print "[Webserver] Recebido: %s do daemon 1" % dados
	finally:
		s.close()
		print "[Webserver] Socket do daemon 1 fechado."

#TODO: criar as threads
encaminhaPacote()
