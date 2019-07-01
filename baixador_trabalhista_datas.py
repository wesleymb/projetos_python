# -*- coding: utf-8 -*-

import time
import os
import shutil
import fnmatch
import argparse
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


path_chromedriver = 'A:\\Baixadores\\BAIXADOR_TRT\\chromedriver.exe'
path_download = os.path.join('A:\\','Baixadores','BAIXADOR_TRT','TRAB_BX')

options = Options()
options.add_experimental_option("prefs", {"download.default_directory": path_download})

def limpar_pasta():
    pasta_de_trab_bx = path_download
    print pasta_de_trab_bx
    lista_de_arq = os.listdir(pasta_de_trab_bx)
    for arq in lista_de_arq:
        try:
            tentar_apagar = os.remove(os.path.join(path_download,arq))
        except:
            try:
                shutil.rmtree(os.path.join(path_download,arq))
            except:
                continue


def temporizador(numero_de_downloads):
    lista_de_downloads_em_andamento = []
    time.sleep(10)
    for root, dirnames, filenames in os.walk(path_download):
        for filename in fnmatch.filter(filenames, '*.crdownload'):
            lista_de_downloads_em_andamento.append(os.path.join(root, filename))
    
    numero_de_downloads_verificados = len(lista_de_downloads_em_andamento)
        
    if numero_de_downloads != numero_de_downloads_verificados and numero_de_downloads_verificados != 0:
        print('Temos {dowload} dowload em andamento...'.format(dowload=numero_de_downloads_verificados))
        temporizador(numero_de_downloads=numero_de_downloads_verificados)            
    elif numero_de_downloads == numero_de_downloads_verificados and numero_de_downloads != 0:
        temporizador(numero_de_downloads=numero_de_downloads_verificados)
    else:
        print('Concluídos...')
    

def criar_pasta_do_tribunai(nome_do_tribunal):
        nome_trt = nome_do_tribunal.encode('cp1252',errors='ignore')
        pasta_do_tribunal = os.path.join(path_download, nome_trt)
        os.makedirs(pasta_do_tribunal) 
        return pasta_do_tribunal
     
def mover_arq(arq,pasta):
    shutil.move(arq,pasta)

def procurar(nome_do_arq):
    for root, dirnames, filenames in os.walk(path_download):
            for filename in fnmatch.filter(filenames, nome_do_arq):
                arq = os.path.join(root, filename)
                return arq    

def organizar_pdf_nas_pastas(lista_de_pastas_dos_tribunais):
 
    pdf_1 = procurar(nome_do_arq='*[0-9].pdf')
    mover_arq(arq=pdf_1,pasta=lista_de_pastas_dos_tribunais[0])
    
    contador = 1

    total_de_pastas = len(lista_de_pastas_dos_tribunais)  
    print('Quantidade de PDF para mover: {pdf}'.format(pdf=total_de_pastas))
    print('Movido {pdf_movido}'.format(pdf_movido=pdf_1))

    for contador in range(1,total_de_pastas):
        pdf = procurar(nome_do_arq='*({contador}).pdf'.format(contador=contador))
        mover_arq(arq=pdf,pasta=lista_de_pastas_dos_tribunais[contador])
        print('Movido {pdf_movido}'.format(pdf_movido=pdf))
        

def baixar_diario_brtst(path_chromedriver,dia,mes,ano):
    def find_element(xpath):
        try:
            return driver.find_element(By.XPATH, xpath)
        except:
            return None
    def click_nas_datas(elemento):
        time.sleep(3)
        elemento_para_clicar = find_element(elemento)
        elemento_para_clicar.click()

    def definir_datas(calendario_site,dia,mes,ano):
        #CALENDARIO INICIAL
        click_nas_datas(elemento='//*[@id="diarioArg"]/fieldset/table/tbody/tr/td[{calendario_site}]/table/tbody/tr/td[1]/span/button/span'.format(calendario_site=calendario_site))
        #ANO
        click_nas_datas(elemento='//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[@value={ano}]'.format(ano=ano))
        #MES
        click_nas_datas(elemento='//*[@id="ui-datepicker-div"]/div[1]/div/select/option[@value={mes}]'.format(mes=mes-1))
        #DIA
        click_nas_datas(elemento='//*[@id="ui-datepicker-div"]/table/tbody/tr/td/a[contains(text(), "{dia}")]'.format(dia=dia))

    
    
    
    driver = webdriver.Chrome(executable_path=path_chromedriver, chrome_options=options)
    driver.get('https://dejt.jt.jus.br/dejt/f/n/diariocon')

    definir_datas(calendario_site=1,dia=dia,mes=mes,ano=ano)
    definir_datas(calendario_site=2,dia=dia,mes=mes,ano=ano)
    
    time.sleep(2)

    pesquisar = find_element('//div[@class="plc-corpo-acao-t" and text()="F9-Pesquisar"]')
    pesquisar.click()
    time.sleep(2)

    downloads = 0
    lista_de_pastas_dos_tribunais = []
    while True:
        for download,nome_do_tribunal in zip(driver.find_elements(By.XPATH, '//button[img[contains(@src, "baixar.png")]]'),driver.find_elements(By.XPATH,'//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[2]')):
            pasta_do_tribunal = criar_pasta_do_tribunai(nome_do_tribunal=nome_do_tribunal.text)
            lista_de_pastas_dos_tribunais.append(pasta_do_tribunal)
            download.click()
            time.sleep(1)
            downloads += 1
        
        proxima_pagina = '//span[@class="ico iNavProximo"]'
        if not find_element(proxima_pagina):
            temporizador(numero_de_downloads=0)
            driver.close()
            organizar_pdf_nas_pastas(lista_de_pastas_dos_tribunais=lista_de_pastas_dos_tribunais)
            break
        else:
            find_element(proxima_pagina).click()
            time.sleep(3)
            nomes_dos_tribunais = driver.find_elements(By.XPATH,'//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[2]')
          
    return downloads        


if __name__ == '__main__':
    hoje = datetime.date.today()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dia",      dest='dia',         type=int, default=hoje.day,     help="Dia")
    parser.add_argument("-m", "--mes",      dest='mes',         type=int, default=hoje.month,   help='M?')
    parser.add_argument("-a", "--ano",      dest='ano',         type=int, default=hoje.year,    help='Ano')
    args = parser.parse_args()
    # args.data = datetime.date(year=args.ano, month=args.mes, day=args.dia)
    
    print(args.dia,args.mes,args.ano)
    print('Iniciando o download dos cadenos trabalhistas...')
    limpar_pasta()
    downloads = baixar_diario_brtst(path_chromedriver,dia=args.dia,mes=args.mes,ano=args.ano)
    print('O total de PDFs baixados foram: {pdf}'.format(pdf=downloads))
    print('Feito!')
 