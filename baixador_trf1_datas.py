#!python2
# -*- coding: utf8

import time
import os
import shutil
import datetime
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


path_chromedriver = 'A:\\Baixadores\\BAIXADOR_TRF1\\chromedriver.exe'
path_download = os.path.join('A:\\','Baixadores','BAIXADOR_TRF1','TRF1_BX')

options = Options()
options.add_experimental_option("prefs", 
                                {"download.default_directory": path_download,
                                "plugins.always_open_pdf_externally": True
                                })


def temporizador():
    lista_de_downloads_em_andamento = []
    time.sleep(5)
    lista_de_arq_path_download = os.listdir(path_download)    
    for arq_path_download in lista_de_arq_path_download:
        if arq_path_download.endswith('.crdownload'):
            lista_de_downloads_em_andamento.append(arq_path_download)
            print 'Downloads em andamento: {}'.format(len(lista_de_downloads_em_andamento)) 
            temporizador()
        else:
            print('Pronto, acabei de baixar...')
            break
            
def limpar_pasta():
    pasta_de_trab_bx = path_download
    print pasta_de_trab_bx
    lista_de_arq = os.listdir(pasta_de_trab_bx)
    for arq in lista_de_arq:
        try:
            os.remove(os.path.join(path_download,arq))
        except:
            try:
                shutil.rmtree(os.path.join(path_download,arq))
            except:
                continue



def baixar_diario_trf1(path_chromedriver,data_download):
    def find_element(xpath):
        try:
            return driver.find_element(By.XPATH, xpath)
        except:
            return None
    
    def find_elements(xpath):
        try:
            return driver.find_elements(By.XPATH, xpath)
        except:
            return None

    def buscar_e_clicar(elemento):
        time.sleep(3)
        elemento_para_clicar = find_element(elemento)
        elemento_para_clicar.click()

    

    driver = webdriver.Chrome(executable_path=path_chromedriver, chrome_options=options)
    driver.get('https://edj.trf1.jus.br/edj/handle/123/3/discover?filtertype_2=dateIssued&filter_relational_operator_2=contains&filter_2=&submit_apply_filter=Aplicar&query=&rpp=17&sort_by=dc.date.issued_dt&order=desc')
    time.sleep(2)

    #MUDAR FILTRO DE BUSCA PARA IGUAL
    buscar_e_clicar('//*[@id="aspect_discovery_SimpleSearch_field_filter_relational_operator_2"]/option[text()="Igual"]')
    #PASSAR DATA PARA O FILTRO
    data_do_filtro = find_element('//*[@id="aspect_discovery_SimpleSearch_field_filter_2"]')
    data_do_filtro.send_keys(data_download)
    buscar_e_clicar('//*[@id="aspect_discovery_SimpleSearch_field_submit_apply_filter"]')
    time.sleep(2)
    
    dowloads= 0
    proxima_pagina = True
    
    while proxima_pagina == True:
        lista_de_download = []
        for i in find_elements('//div[@class="artifact-title"]/a[contains(text(), "{data}")]'.format(data=data_download)):
            lista_de_download.append(i.text)
    
        
        for link_caderno in lista_de_download:
            link_caderno = link_caderno.encode('utf8')
            print('{like}'.format(like=link_caderno))
            caderno = find_element('//div[@class="artifact-title"]/a[text()="{}"]'.format(link_caderno))
            caderno.click()
            time.sleep(2)
            

            lista_de_link_pdf = find_elements('//*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/div/div/div[2]/div/ul/li[4]/a')
            
            for link_pdf in lista_de_link_pdf:
                link_pdf.click()
                time.sleep(3)
                dowloads = dowloads + 1
            
            driver.execute_script("window.history.go(-1)")
            time.sleep(2)

        try :
            if buscar_e_clicar('//*[@id="aspect_discovery_SimpleSearch_div_search"]/div[4]/ul/li[3]/a[contains(text(), "Próxima página")]'):
                proxima_pagina = True
        except:
            proxima_pagina = False
    
    
    return dowloads     
    


if __name__ == '__main__':
    print('Iniciando o download dos cadenos TRF1...')
    limpar_pasta()
    hoje = datetime.date.today()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dia",      dest='dia',         type=int, default=hoje.day,     help="Dia")
    parser.add_argument("-m", "--mes",      dest='mes',         type=int, default=hoje.month,   help='Mês')
    parser.add_argument("-a", "--ano",      dest='ano',         type=int, default=hoje.year,    help='Ano')
    args = parser.parse_args()
    args.data = datetime.date(year=args.ano, month=args.mes, day=args.dia)
      
    print 'Data de Download: {data}'.format(data=args.data)
    dowloads = baixar_diario_trf1(path_chromedriver=path_chromedriver,data_download='{data}'.format(data=args.data))
    temporizador()
    print('O total de dowloas foi: {dowload}'.format(dowload=dowloads))
    
    
 