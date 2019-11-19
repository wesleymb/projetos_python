#!python3
# -*- coding: utf8

import os
import sqlite3

#SQL

def criar_banco():
	arquivos = os.listdir()
	if 'bd_mdm.db' not in arquivos:
		connection = sqlite3.connect('bd_mdm.db')
		connection.cursor()
		create_table_clientes()
		create_table_email_para_envio()

def create_table_email_para_envio():
	pasta_padrao = os.path.join(os.environ['USERPROFILE'],'Desktop')	
	connection = sqlite3.connect('bd_mdm.db')
	c = connection.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS Email_Para_Envio (EmailDeEnvio text, SenhaDeEnvio text, Titulo text, TextoDoEmail text, NomeDoArquivo text ,PastaDeEnvio text)')
	c.execute("INSERT INTO Email_Para_Envio VALUES ('teste', '123456', 'Titulo', 'Exemplo de texto','recortes.doc','{pasta}')".format(pasta=pasta_padrao))
	connection.commit()

def create_table_clientes():
	connection = sqlite3.connect('bd_mdm.db')
	c = connection.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS Cliente (IdCliente text, NomeCliente text, EmailCliente text, NumeroDeTelefoneCliente text,StatusCliente text, Servico text, DataDeInclusao date, DadosExtra text, DataDoEnvio date)')
	c.execute("INSERT INTO Cliente VALUES ('a0001', 'teste1', 'teste@teste.com','2222-2222','ATIVO','IMPRIMIR', '1991-03-05', 'Dados extra','')")
	c.execute("INSERT INTO Cliente VALUES ('a0002', 'teste2', 'teste@teste.com','2222-2222','ATIVO','EMAIL', '1991-03-05', 'Dados extra','')")
	c.execute("INSERT INTO Cliente VALUES ('a0003', 'teste3', 'teste@teste.com','2222-2222','INATIVO','IMPRIMIR-EMAIL', '1991-03-05','Dados extra','')")
	connection.commit()

def conectar():
	connection = sqlite3.connect('bd_mdm.db')
	c = connection.cursor()
	return c,connection

def ler_banco(tabela):
	c,connection = conectar()
	sql = 'SELECT * FROM {tabela}'.format(tabela=tabela)
	for linha in c.execute(sql):
		print(linha)
	print('\n')
	connection.commit()

def query_de_id_clinte(id_cliente):
	c,connection = conectar()
	sql = "SELECT * FROM cliente WHERE IdCliente = '{id}'".format(id=id_cliente)
	for dado in c.execute(sql):
		return dado
	connection.commit()

def query_de_update_de_dados_cliente(id_cliente,campo,dado_de_entrada):
	c,connection = conectar()
	c.execute("SELECT * FROM cliente")  
	c.execute("UPDATE cliente SET {campo} = '{dado}' WHERE IdCliente = '{id}'".format(campo=campo, dado=dado_de_entrada,id=id_cliente))
	connection.commit()   

