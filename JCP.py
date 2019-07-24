#!python2
# -*- coding: latin-1
import sys
sys.path.append ('L:\\base\\lib')

import wx
import wx.calendar
import os
import shutil
import time
import datetime
import subprocess
import re
import webbrowser

import cPickle as pickle

from threading import * 
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lido.defs import db_sys_engine
from lido.models.sys import Caderno,DadosCaderno

import lido.models.sys as sm

db_sys_engine = create_engine('postgresql://postgres:c1qdFpfF@192.168.32.5:5432/lido')
Session = sessionmaker(bind=db_sys_engine)


CADENOS_DO_P = [
            'ACJF',
            'ACMP',
            'ACTRE1',
            'ALCO',
            'ALDJ',
            'ALJF',
            'ALTRE1',
            'AMDJ',
            'AMJF',
            'AMMP',
            'ANGRAMU1',
            'APDJ',
            'APJF',
            'APTRE1',
            'ARACAJUMU1',
            'BAJF',
            'BALEG',
            'BAMU1',
            'BARUERIMU1',
            'BATCM',
            'BATRE1',
            'BELMU1',
            'BETIMMU1',
            'BHMU1',
            'BOAVISTAMU1',
            'CAMPDO',
            'CAMPOSMU1',
            'CAMRIO',
            'CARIACICAMU1',
            'CEDJ',
            'CEJF',
            'CETRE1',
            'CGRANDEMU1',
            'CNJBR',
            'CNMP1',
            'CONTAGEMMU1',
            'CORRENTINAMU1',
            'CTBAMU1',
            'DEC1',
            'DFJF',
            'DFTRE1',
            'DTM1',
            'EEBRSTF',
            'EEBRTST',
            'EEDF1',
            'EEDO1',
            'EEDO2',
            'EEDO3',
            'EEEPMA',
            'EEESDJ',
            'EEEXGO1',
            'EEEXMA1',
            'EEMGFI',
            'EEPOAMU1',
            'EERJTRE1',
            'EERJTRT',
            'EERS1',
            'EESPTRT',
            'EESPTRT2',
            'EETO1',
            'EETRF4',
            'EPCE',
            'EPMA',
            'EPMALIC',
            'EPPB',
            'EPPR',
            'EPTO',
            'ESDO',
            'ESMU1',
            'ESTRE1',
            'EXAM1',
            'EXAP1',
            'EXCE1',
            'EXCE2',
            'EXGO1',
            'EXMA1',
            'EXMSLIC',
            'EXPB1',
            'EXPI1',
            'EXPR1',
            'EXRO1',
            'EXRR1',
            'EXSC1',
            'FLORIPAMU1',
            'FORMU1',
            'GOIMU1',
            'GOJF',
            'GOLEG',
            'GOMP',
            'GOMP2',
            'GOTRE1',
            'GRMU1',
            'GVALADARESMU1',
            'INDAIATUBAMU1',
            'JPESSOAMU1',
            'JUNDIAIMU1',
            'LDEFREITASMU1',
            'LEMEMU1',
            'LIMEIRAMU1',
            'MAJF',
            'MANAUSMU1',
            'MATRE1',
            'MGAD',
            'MGED',
            'MGFB',
            'MGFI',
            'MGJF',
            'MGLEG',
            'MGMP',
            'MGSI',
            'MGSISI',
            'MGTRE1',
            'MPF1',
            'MSDO',
            'MSLEG',
            'MSMU1',
            'MSTRE1',
            'MTDJ',
            'MTDO',
            'MTJF',
            'MTMU1',
            'MTTRE1',
            'MUNICIPIOSAM',
            'MUNICIPIOSRJ',
            'NATALMU1',
            'NIGUACUMU1',
            'NOVAFRIBURGOMU1',
            'OABNAC',
            'PADO',
            'PAJF',
            'PALMASMU1',
            'PAMULIC',
            'PATRE1',
            'PBJF',
            'PBTRE1',
            'PEJF',
            'PIJF',
            'PIRACICABAMU1',
            'PORTOVELHOMU1',
            'PRLEG',
            'PRMULIC',
            'RJDP',
            'RJJC',
            'RJLEG',
            'RJMP',
            'RJP5',
            'RJTRE1',
            'RNAD',
            'RNDJ2',
            'RNJF',
            'RNTRE1',
            'ROJF',
            'ROTRE1',
            'RPIS1',
            'RPIS2',
            'RRDJ',
            'RRJF',
            'RRTRE1',
            'RSAD',
            'RSDJ1',
            'RSDJ1SI',
            'RSDJ2',
            'RSDJ3',
            'RSDJ4',
            'RSLEG',
            'RSTRE1',
            'SANTOANDREMU1',
            'SANTOSMU1',
            'SBCAMPOMU1',
            'SCDJ',
            'SCDJSI',
            'SCLEG',
            'SCMULIC',
            'SCTRE1',
            'SDEPARNAIBAMU1',
            'SEDJ',
            'SEFAM',
            'SEFMG',
            'SEFSE',
            'SEJF',
            'SENADO1',
            'SETELAGOASMU1',
            'SJDOSCAMPOSMU1',
            'SJDOSPINHAISMU1',
            'SJMERITIMU1',
            'SLUIZMU1',
            'SOROCABAMU1',
            'SPJM1',
            'SUMAREMU1',
            'SUZANOMU1',
            'TAUBATEMU1',
            'TCAC1',
            'TCAL1',
            'TCAM1',
            'TCAP1',
            'TCBA1',
            'TCCE1',
            'TCES1',
            'TCGO1',
            'TCMA1',
            'TCMBE',
            'TCMG1',
            'TCMS1',
            'TCPR1',
            'TCPR1A',
            'TCRO1',
            'TCRS1',
            'TCSC1',
            'TCSE1',
            'TCTO1',
            'TCUBOLETIM',
            'TERESINAMU1',
            'TODJ',
            'TOJF',
            'TOTRE1',
            'TRF1A',
            'TRF5I',
            'UBERABAMU1',
            'VITORIAESMU1',
            'VREDONDAMU1',
            'VTCMU1',
        ]


def main():
   
    p = UI_JCP(None)
    p.start()

class UI_GERADOR_DE_NNX_POR_INTERVALOS(Thread,object):
    """docstring for UI_GERADOR_DE_NNX_POR_INTERVALOS"""
    def __init__(self):
        super(UI_GERADOR_DE_NNX_POR_INTERVALOS, self).__init__()
        
        self.frame = wx.Frame(None, -1, 'Gerador de cadernos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,600,225)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        
        wx.StaticBox(self.panel, wx.ID_ANY, 'Parâmetros de criação', (10, 5), size=(425, 180))
        
        self.button_buscar_caderno = wx.Button(self.panel, wx.ID_ANY, 'Selecionar caderno', (25, 20))    
        self.button_buscar_caderno.Bind(wx.EVT_BUTTON, self.buscar_nnx)
        self.box_caderno_nnx = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(400,-1),style=wx.TE_READONLY)

        self.button_buscar_intervalo = wx.Button(self.panel, wx.ID_ANY, 'Selecionar inervalo', (25, 85))    
        self.button_buscar_intervalo.Bind(wx.EVT_BUTTON, self.buscar_txt)
        self.box_caderno_intervalo = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 115),size=(400,-1),style=wx.TE_READONLY)
        
        
        self.texto_novo_caderno = wx.StaticText(self.panel, wx.ID_ANY, "Novo caderno:", (25, 150))
        self.box_novo_caderno = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 150),size=(200,-1))
        
        self.button_buscar_intervalo = wx.Button(self.panel, wx.ID_ANY, 'Criar', (475, 50),size=(100,70))
        self.button_buscar_intervalo.Bind(wx.EVT_BUTTON, self.criar_no_caderno)
        
        self.frame.Show()
        self.frame.Centre()

    

    def criar_no_caderno(self,event):
        caderno_novo = self.box_novo_caderno.GetLineText(0).upper()
        if caderno_novo != '': 
            comando = 'A:\\LIDO\\cmd\\gera_cad_dist.py -n {caderno} -i {intervalo} -nc {nome_do_novo_caderno}'.format(caderno=self.diretorio_caderno, intervalo=self.diretorio_intervalo, nome_do_novo_caderno=caderno_novo)
            if os.system(comando):
                erro = '############\n Erro \n############\n'

            self.box_novo_caderno.SetValue('')
            self.box_caderno_intervalo.SetValue('')
            self.box_caderno_nnx.SetValue('')
            self.diretorio_caderno = None
            self.diretorio_intervalo = None
            dlg_box_p = wx.MessageDialog(None , "Pronto, caderno criado em C:\\tmp","Pronto...", wx.OK|wx.ICON_INFORMATION)
            dlg_box_p.ShowModal()
        else:
            dlg_box_p = wx.MessageDialog(None , "Como posso criar um caderno sem nome?","Sem nome.", wx.OK|wx.ICON_QUESTION)
            dlg_box_p.ShowModal()

    def buscar_nnx(self,event):
        self.buscar(tipo_de_arquivo='nnx')

    def buscar_txt(self,event):
        self.buscar(tipo_de_arquivo='txt')
    
    def buscar(self,tipo_de_arquivo):
        openFileDialog = wx.FileDialog(self.frame, "Selecione o {tipo}".format(tipo=tipo_de_arquivo), "", "", 
                                      "Arquivos de nnx (*.{tipo1})|*.{tipo2}".format(tipo1=tipo_de_arquivo,tipo2=tipo_de_arquivo.upper()), 
                                      wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
 
        openFileDialog.ShowModal()
        try:
            if openFileDialog.GetPaths() != '' or openFileDialog.GetPaths() != None:
                if tipo_de_arquivo == 'nnx':
                    self.diretorio_caderno = ''.join(openFileDialog.GetPaths()) 
                    self.box_caderno_nnx.SetValue( self.diretorio_caderno)
                
                if tipo_de_arquivo == 'txt':
                    self.diretorio_intervalo = ''.join(openFileDialog.GetPaths())
                    self.box_caderno_intervalo.SetValue(self.diretorio_intervalo)

        except:
            openFileDialog.Destroy()


class UI_COMANDO_PM(Thread,object):
    """docstring for UI_COMANDO_PM"""
    def __init__(self):
        super(UI_COMANDO_PM, self).__init__()
        self.frame = wx.Frame(None, -1, 'Comando PM', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,275,225)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)

        wx.StaticBox(self.panel, wx.ID_ANY, 'Parâmetros de preparção', (5, 5), size=(250, 185))
        self.texto_calendario_pasta_rotina = wx.StaticText(self.panel, wx.ID_ANY, "Pasta rotina", (25, 75))
        self.calendario_pasta_rotina = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 100),style=wx.DP_DROPDOWN)

        
        
        self.checkbox_do_p =  wx.CheckBox(self.panel, wx.ID_ANY, "Para o dia (-p):", (150, 75))
        self.checkbox_do_p.Bind(wx.EVT_CHECKBOX,self.validar_p_checkbox)
        self.calendario_comando_p = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (150, 100),style=wx.DP_DROPDOWN)
        self.calendario_comando_p.Enable(False)
        
        self.texto_caderno = wx.StaticText(self.panel, wx.ID_ANY, "Caderno", (25,25))
        self.box_caderno = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 40),size=(200,-1))

        
        self.button_verificar = wx.Button(self.panel, wx.ID_ANY, 'Preparar', (80, 130),size=(100,50))
        self.button_verificar.Bind(wx.EVT_BUTTON, self.preparar)
                
        self.frame.Show()
        self.frame.Centre()


    def criar_relatorio_txt(self,caderno,dia,mes,ano,status_p):
        data_de_relatorio = datetime.datetime.now()
        r_dia,r_mes,r_ano = data_de_relatorio.strftime('%d'),data_de_relatorio.strftime('%m'),data_de_relatorio.strftime('%Y')
        with open((os.path.join('A:\\','Baixadores','JCP','Relatorio_JCP','{dia}-{mes}-{ano}-relatorio.txt'.format(dia=r_dia,mes=r_mes,ano=r_ano))), 'a+t') as arq_txt:
                
                linha_do_caderno = '\nCaderno: {Caderno}\n'.format(Caderno=caderno)
                arq_txt.write(linha_do_caderno)
                
                data_pasta_de_rotina = 'Dados da pasta Rotina: {dia}/{mes}/{ano}\n'.format(dia=dia,mes=mes,ano=ano)
                arq_txt.write(data_pasta_de_rotina)

                dados_de_preparacao = 'Dados de preparação: {}\n'.format(data_de_relatorio.strftime('%c'))
                arq_txt.write(dados_de_preparacao)

                linha_do_p = 'Para o dia (-p): {status}\n'.format(status=status_p)
                arq_txt.write(linha_do_p)
                
    
    
    
    def validar_p_checkbox(self,event):
        if self.checkbox_do_p.Value == False:
            self.calendario_comando_p.Enable(False)
        else:
            self.calendario_comando_p.Enable(True)
    
    
    def gera_data(self,calendario):
        data = calendario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data_ajustada
    
    def criar_dia_mes_ano(self,data):
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')


    def chamar_pm(self):
        
        data_rotina = self.gera_data(calendario=self.calendario_pasta_rotina)
        dia,mes,ano = self.criar_dia_mes_ano(data=data_rotina)    
        caderno = self.box_caderno.GetLineText(0).upper()
        
        
        
        if self.checkbox_do_p.Value == True:
            data_p = self.gera_data(calendario=self.calendario_comando_p)
            dia_p,mes_p,ano_p = self.criar_dia_mes_ano(data=data_p)
            data_do_p = '{dia}/{mes}/{ano}'.format(dia=dia_p,mes=mes_p,ano=ano_p)
            # print(caderno,dia,mes,ano,data_do_p)
            todos_os_comandos = ['A', 'pm {caderno} -d {dia} -m {mes} -a {ano} -p {para_o_dia}'.format(caderno = caderno, dia = dia, mes = mes, ano = ano, para_o_dia = data_do_p)]
            cmd_str = '\n'.join(todos_os_comandos)+'\n'
            p = subprocess.Popen('cmd.exe', shell=True, cwd=r'a:\lido\cmd', stdin=subprocess.PIPE)
            p.stdin.write(cmd_str)
            self.box_caderno.SetValue('')
            self.criar_relatorio_txt(caderno=caderno,dia=dia,mes=mes,ano=ano,status_p=data_do_p)
        
        if self.checkbox_do_p.Value == False:
            if caderno not in CADENOS_DO_P:
                todos_os_comandos = ['A', 'pm {caderno} -d {dia} -m {mes} -a {ano}'.format(caderno = caderno, dia = dia, mes = mes, ano = ano)]
                cmd_str = '\n'.join(todos_os_comandos)+'\n'
                p = subprocess.Popen('cmd.exe', shell=True, cwd=r'a:\lido\cmd', stdin=subprocess.PIPE)
                p.stdin.write(cmd_str)
                self.box_caderno.SetValue('')
                self.criar_relatorio_txt(caderno=caderno,dia=dia,mes=mes,ano=ano,status_p='')
            else:
                dlg_box_p = wx.MessageDialog(None , "Esse caderno tem o -p ou não estou conseguindo preparar.","Ops..", wx.OK| wx.ICON_WARNING)
                dlg_box_p.ShowModal()
    
    
    def preparar(self,event):
        self.caderno = self.box_caderno.GetLineText(0).upper()
        self.chamar_pm()
        



class UI_ANALISADOR_DE_CONJUNTOS(Thread,object):
    """docstring for UI_ANALISADOR_DE_CONJUNTOS"""
    def __init__(self, arg):
        super(UI_ANALISADOR_DE_CONJUNTOS, self).__init__()
        self.frame = wx.Frame(None, -1, 'Analisador de conjuntos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,625,600)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.index = 0
        self.total_geral = 0

        wx.StaticBox(self.panel, wx.ID_ANY, 'Parâmetros de análise', (10, 5), size=(325, 185))
        wx.StaticBox(self.panel, wx.ID_ANY, 'Dados do conjunto', (340, 5), size=(270, 185))

        self.button_analisar = wx.Button(self.panel, wx.ID_ANY, 'Analisar conjunto', (25, 150))
        self.button_analisar.Bind(wx.EVT_BUTTON, self.analisar)
        
        
        self.checkbox_conjunto =  wx.CheckBox(self.panel, wx.ID_ANY,  "Conjuntos:", (25, 85))
        self.checkbox_conjunto.Bind(wx.EVT_CHECKBOX,self.habilitar_box_conjunto)
        self.checkbox_conjunto.SetValue(True)

        self.box_conjunto = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 105),style=wx.TE_PROCESS_ENTER)
        self.box_conjunto.Bind(wx.EVT_TEXT_ENTER, self.analisar)


        self.texto_spin_relevancia = wx.StaticText(self.panel, wx.ID_ANY, "Relevância do caderno:", (150, 30))
        self.spin_relevancia = wx.SpinCtrl(self.panel, wx.ID_ANY, pos =(225, 55),min=0, max=100, initial=3,size=(50,-1),style=wx.SP_ARROW_KEYS) 

        self.texto_percentual_de_desmarcacao = wx.StaticText(self.panel, wx.ID_ANY, "Percentual de desmarcação:", (150, 80))
        self.spin_percentual_de_desmarcacao = wx.SpinCtrl(self.panel, wx.ID_ANY, pos =(225, 105),min=0, max=100, initial=3,size=(50,-1),style=wx.SP_ARROW_KEYS)


        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data:", (25, 30))
        self.calendario = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 50),style=wx.DP_DROPDOWN)

        self.box_para_print = wx.TextCtrl(self.panel, wx.ID_ANY,"", (350, 30),size=(250, 150),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)
        
        self.lista_de_dados = wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(572,350),pos=(25, 200))      
        self.lista_de_dados.InsertColumn(0,"Parceira")
        self.lista_de_dados.InsertColumn(1,"Conjunto")
        self.lista_de_dados.InsertColumn(2,"Caderno")
        self.lista_de_dados.InsertColumn(3,"Ocorrências")
        self.lista_de_dados.InsertColumn(4,"Desmarcados")
        self.lista_de_dados.InsertColumn(5,"Precentual de desmarcados")
        self.lista_de_dados.InsertColumn(6,"Relevancia",width=100)       
        
        self.frame.Show()
        self.frame.Centre()

    def habilitar_box_conjunto (self,event):
        if self.checkbox_conjunto.Value == False:
            self.box_conjunto.Enable(False)
            self.box_conjunto.SetValue("")
        if self.checkbox_conjunto.Value == True:
            self.box_conjunto.Enable(True)

    def definir_conjuntos(self,event,pasta):
        lista_de_conjuntos = []
        
        pastas = os.listdir(pasta)
        for pasta in pastas:
            conjunto = re.search(r'^(1_)([0-9]{1,})', pasta)
            if conjunto:       
                lista_de_conjuntos.append(conjunto.group(2))

            
        return sorted(lista_de_conjuntos)

    def formar_pasta(self,event,dia,mes,ano):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'dados')


    def printar_na_box(self, event,texto):
        self.box_para_print.AppendText(texto)
        self.box_para_print.AppendText('\n')    
    
    
    
    def verificar_relatorios_pco(self,event,parceira_id,conjunto,dia, mes, ano,relevancia,percentual_de_desmarcacao):
        ret = []
        ret_final = []
        qtd_total = 0
        qtd_total_desmarcado = 0
        

        session = sessionmaker(bind=db_sys_engine)()
        ROTINA_BASE_DIR = r'L:\rotina'
        BASE_LIB_DIR = r'L:\base\lib\lido'


        diretorio = os.path.join(ROTINA_BASE_DIR, ano, mes, dia, 'dados', '{}_{}'.format(parceira_id,conjunto))
        for root, dirs, files in os.walk(diretorio):
            if root.endswith('rel'):
                parceira = session.query(sm.Parceira).filter(sm.Parceira.id==parceira_id).one().nome.encode('latin-1')
                for arq in files:
                    caderno = arq.split('.')[0].upper()
                    arquivo_rel = os.path.join(root, arq)
                    with open(arquivo_rel) as fd:
                        rel = pickle.load(fd)
                        qtd = len(rel.ocorrencias)
                        desmarcados = len([x for x in rel.ocorrencias if not x.resultado_das_avaliacoes])
                        try:
                            perc_desmarcado = int(desmarcados*100.0/qtd)
                        except:
                            perc_desmarcado = 0
                            
                        dado = (parceira, conjunto, caderno, qtd, desmarcados, perc_desmarcado)
                        if qtd:
                            qtd_total = int(qtd_total + qtd)
                            qtd_total_desmarcado = int(qtd_total_desmarcado + desmarcados)
                            ret.append(dado)
                            self.total_geral = self.total_geral + qtd 

        self.printar_na_box(event=event,texto='Conjunto: {}'.format(conjunto))
        self.printar_na_box(event=event,texto='Total de ocorrências: {}'.format(qtd_total))
        self.printar_na_box(event=event,texto='Total de desmarcação: {}'.format(qtd_total_desmarcado))
        proc_desmarc = float(qtd_total_desmarcado*100.0/qtd_total)
        self.printar_na_box(event=event,texto='Percentual de desmarcação: {}%'.format(round(proc_desmarc,3)))
        self.printar_na_box(event=event,texto='----------------------------------------') 
        for dados_do_caderno in ret:
            qtd_do_caderno = float(dados_do_caderno[3])
            relatevancia = float(qtd_do_caderno*100/qtd_total)
            relatevancia = round(relatevancia,3)
            # print(dados_do_caderno[0],dados_do_caderno[1],dados_do_caderno[2],dados_do_caderno[3],dados_do_caderno[4],dados_do_caderno[5],relatevancia)
            if relatevancia >= relevancia:
                if dados_do_caderno[5] >= percentual_de_desmarcacao:
                    dados_para_purga = (dados_do_caderno[0],dados_do_caderno[1],dados_do_caderno[2],dados_do_caderno[3],dados_do_caderno[4],dados_do_caderno[5],relatevancia)
                    ret_final.append(dados_para_purga)

        return ret_final
    
    def criar_dia_mes_ano(self,event,data):
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')
    
    
    def gera_data(self,event,caledario):
        data = caledario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data_ajustada
    def apagar_lista(self,event):
        self.lista_de_dados.DeleteAllItems() 
    


    def analisar(self,event):
        self.total_geral = 0
        lista_de_conjuntos = []

        data = self.gera_data(event = event, caledario = self.calendario)
        dia,mes,ano = self.criar_dia_mes_ano(event = event,data=data)
       
        if self.box_conjunto.GetLineText(0) != '' and self.checkbox_conjunto.Value == True:
            lista_de_conjuntos.append(self.box_conjunto.GetLineText(0))
        
        if self.box_conjunto.GetLineText(0) == '' and self.checkbox_conjunto.Value == True:
            dlg_box_box_conjunto = wx.MessageDialog(None , "Se võce não me der nem um conjunto \nnão há o que analisar.","Ops...", wx.OK| wx.ICON_QUESTION) 
            dlg_box_box_conjunto.ShowModal()
            
        if self.checkbox_conjunto.Value == False:
            pasta = self.formar_pasta(event=event,dia=dia,mes=mes,ano=ano)
            lista_de_conjuntos = self.definir_conjuntos(event=event,pasta=pasta)

        relevancia = self.spin_relevancia.GetValue()
        percentual_de_desmarcacao = self.spin_percentual_de_desmarcacao.GetValue()
        self.box_para_print.SetValue('')
        self.box_conjunto.SetValue('')
        self.apagar_lista(event=event)
        self.index = 0

        max = len(lista_de_conjuntos)
        count = 0
        dlg_carregar = wx.ProgressDialog("Processando", "Tempo estimado", max, parent=self.frame ,style= wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
            
        for conjunto in lista_de_conjuntos:
            count = count + 1
            try:
                dados = self.verificar_relatorios_pco(event=event,parceira_id=1,conjunto=conjunto,dia=dia, mes=mes, ano=ano,relevancia=relevancia,percentual_de_desmarcacao=percentual_de_desmarcacao)
                for dado in sorted(dados):
                    self.lista_de_dados.InsertStringItem(self.index, dado[0])
                    self.lista_de_dados.SetStringItem(self.index, 1, str(dado[1]))
                    self.lista_de_dados.SetStringItem(self.index, 2, str(dado[2]))
                    self.lista_de_dados.SetStringItem(self.index, 3, str(dado[3]))
                    self.lista_de_dados.SetStringItem(self.index, 4, str(dado[4]))
                    self.lista_de_dados.SetStringItem(self.index, 5, '{}%'.format(str(dado[5])))
                    self.lista_de_dados.SetStringItem(self.index, 6, '{}%'.format(str(dado[6])))
                    self.index += 1

            except:
                dlg_box_box_conjunto = wx.MessageDialog(None , "Acho que não temos ocorrências\npara esse conjunto neste dia.","Sem occorência...", wx.OK| wx.ICON_QUESTION) 
                dlg_box_box_conjunto.ShowModal()
                self.printar_na_box(event=event,texto='----------------------------------------')
        
            if count < max:
                dlg_carregar.Update(count)
            else:
                dlg_carregar.Update(False)
                
        dlg_carregar.Destroy()
        
        
        if self.checkbox_conjunto.Value == False:
            self.printar_na_box(event=event,texto='Total de ocorrências: {total}'.format(total=self.total_geral))
        
        dlg_box_box_conjunto = wx.MessageDialog(None , "Pronto, análise feita","Concluída", wx.OK| wx.ICON_QUESTION) 
        dlg_box_box_conjunto.ShowModal()
        

class UI_LER_PCO_AUTO(Thread,object):
    """docstring for UI_LER_PCO_AUTO"""
    def __init__(self, arg):
        super(UI_LER_PCO_AUTO, self).__init__()
        self.frame = wx.Frame(None, -1, 'Ler intervalo de datas', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,300,200)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)

        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data inicial:", (25, 25))
        self.calendario_inicial = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 50),style=wx.DP_DROPDOWN)

        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data final:", (150, 25))
        self.calendario_final = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (150, 50),style=wx.DP_DROPDOWN)

        self.box_conjunto = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 80),size=(200,-1))

        self.button_verificar = wx.Button(self.panel, wx.ID_ANY, 'Ler conjunto', (25, 115))
        self.button_verificar.Bind(wx.EVT_BUTTON, self.ler_tudo)
                
        self.frame.Show()
        self.frame.Centre()

    
    def criar_dia_mes_ano(self,event,data):
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')
    
    
    def gera_data(self,event,caledario):
        data = caledario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data_ajustada
    
    
    def calcular_intervalo_de_datas(self,event,data_inicial,data_final):
        dif_de_datas = []
        if data_inicial == data_final:
            dif_de_datas.append(data_inicial)
        if data_inicial != data_final:  
            dif_de_datas.append(data_inicial)
            while data_final > data_inicial:
                data_inicial = data_inicial.fromordinal(data_inicial.toordinal()+1)
                dif_de_datas.append(data_inicial)
        
        return dif_de_datas

    
    def ler_tudo(self,event):
        data_inicial = self.gera_data(event = event, caledario = self.calendario_inicial)
        data_final = self.gera_data(event = event, caledario = self.calendario_final)
        
                
        if data_final != data_inicial: 
            dia_final,mes_final,ano_final = self.criar_dia_mes_ano(event= event, data = data_final)
            datas = self.calcular_intervalo_de_datas(event = event, data_inicial = data_inicial, data_final = data_final)
        else:
            datas = [data_inicial]

        for data in datas:
            dia,mes,ano = self.criar_dia_mes_ano(event= event, data = data)
            event.Skip()
            os.spawnv(os.P_WAIT, r'C:\Python27\python.exe', ['python', '-u', r'L:\base\b\pco\leitor.py', str(78), str(1), str(self.box_conjunto.GetLineText(0)), str(dia), str(mes), str(ano)])
        self.box_conjunto.SetValue('')
        dlg_pronto = wx.MessageDialog(None , "Pronto, leitura Concluída.","Fim da leitura.", wx.OK| wx.ICON_INFORMATION) 
        dlg_pronto.ShowModal()


class UI_conferir_pdf_com_nnx(Thread,object):
    """docstring for UI_conferir_pdf_com_nnx"""
    def __init__(self, arg):
        super(UI_conferir_pdf_com_nnx, self).__init__()
        
        self.lista_de_cadernos_tipo_pdf = []
        self.lista_de_cadernos_tipo_dia = []
        self.lista_de_divergencia = []
        
        self.cadernos_que_nao_conferem = [
        'CUIABAMU1',
        'TRF1SI',
        ]
        
        
        self.frame = wx.Frame(None, -1, 'Conferir PDF com NNX', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,600,400)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        
        self.button_verificar = wx.Button(self.panel, wx.ID_ANY, 'Verifica', (25, 100))
        self.button_verificar.Bind(wx.EVT_BUTTON, self.conferir_pdfs_com_nnx)
        
        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data inicial:", (25, 25))
        self.calendario_inicial = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 50),style=wx.DP_DROPDOWN)
        

        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data final:", (150, 25))
        self.calendario_final = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (150, 50),style=wx.DP_DROPDOWN)
        
        self.box_para_print = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 125),size=(550, 225),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)
        
        self.frame.Show()
        self.frame.Centre()
    
    def montar_lista_de_caderno_tipo_dia(self,event,pasta):
        for arquivo_da_pasta_de_cadernos_preparados in pasta:
            arquivo_nnx = re.search(r'(^(.*)(\.)([Dd][Ii][Aa]$))',arquivo_da_pasta_de_cadernos_preparados)
            if  arquivo_nnx:
                if arquivo_nnx.group(2).upper() not in self.cadernos_que_nao_conferem:
                    self.lista_de_cadernos_tipo_dia.append(arquivo_nnx.group(2).upper())
                    
    
    def montar_lista_de_caderno_tipo_pdf(self,event,pasta):
        for arquivo_da_pasta_rotina in pasta:
            if re.search(r'(^[A-Za-z0-9]{2,}$)',arquivo_da_pasta_rotina):
                if arquivo_da_pasta_rotina not in self.cadernos_que_nao_conferem:
                    self.lista_de_cadernos_tipo_pdf.append(('{caderno}'.format(caderno=arquivo_da_pasta_rotina)).upper())
    
    def consultar_arquivos_aquivos_na_pasta(self,event,pasta):
        return os.listdir(pasta)
    
    def formar_pasta_de_cadernos_preparados(self,event,dia,mes,ano):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'cadernos')

    def formar_pasta_de_download_do_caderno(self,event,dia,mes,ano):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'download')

    
    def criar_dia_mes_ano(self,event,data):
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')
    
    def calcular_intervalo_de_datas(self,event,data_inicial,data_final):
        dif_de_datas = []
        if data_inicial == data_final:
            dif_de_datas.append(data_inicial)
        if data_inicial != data_final:  
            dif_de_datas.append(data_inicial)
            while data_final > data_inicial:
                data_inicial = data_inicial.fromordinal(data_inicial.toordinal()+1)
                dif_de_datas.append(data_inicial)
        
        return dif_de_datas   
    
    
    def printar_na_box(self, event,texto):
        self.box_para_print.AppendText(texto)

    
    def gera_data(self,event,caledario):
        data = caledario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data_ajustada
    
    def conferir_pdfs_com_nnx(self,event):
        
        self.box_para_print.SetValue('')

        
        data_inicial = self.gera_data(event = event, caledario = self.calendario_inicial)
        data_final = self.gera_data(event = event, caledario = self.calendario_final)

        dia_inicial,mes_inicial,ano_inicial = self.criar_dia_mes_ano(event= event, data = data_inicial)
        
        self.printar_na_box(event= event, texto='Data inicial: ')
        self.printar_na_box(event= event, texto='{dia}/{mes}/{ano}\n'.format(dia=dia_inicial,mes=mes_inicial,ano=ano_inicial))
        if data_final != data_inicial: 
            self.printar_na_box(event= event, texto='Data final: ')
            dia_final,mes_final,ano_final = self.criar_dia_mes_ano(event= event, data = data_final)
            self.printar_na_box(event= event, texto='{dia}/{mes}/{ano}\n'.format(dia=dia_final,mes=mes_final,ano=ano_final))
            datas = self.calcular_intervalo_de_datas(event = event, data_inicial = data_inicial, data_final = data_final)
        else:
            datas = [data_inicial]

        for data in datas:
            try:
                self.lista_de_cadernos_tipo_pdf = []
                self.lista_de_cadernos_tipo_dia = []
                self.lista_de_divergencia = []

                dia,mes,ano = self.criar_dia_mes_ano(event= event, data = data)
                pasta_de_rotina = self.formar_pasta_de_download_do_caderno(event=event,dia=dia,mes=mes,ano=ano)
                pasta_de_cadernos_preparados = self.formar_pasta_de_cadernos_preparados(event=event,dia=dia,mes=mes,ano=ano)
                arquivos_na_pasta_rotina = self.consultar_arquivos_aquivos_na_pasta(event=event,pasta=pasta_de_rotina)
                arquivos_na_pasta_de_cadernos_preparados = self.consultar_arquivos_aquivos_na_pasta(event=event,pasta=pasta_de_cadernos_preparados)
                self.montar_lista_de_caderno_tipo_pdf(event=event,pasta=arquivos_na_pasta_rotina)
                self.montar_lista_de_caderno_tipo_dia(event=event,pasta=arquivos_na_pasta_de_cadernos_preparados)
                
                
                self.printar_na_box(event= event, texto='\n')
                self.printar_na_box(event= event, texto='\nData: {dia}/{mes}/{ano}\n'.format(dia=dia,mes=mes,ano=ano))
                
                for cadeno_dia in self.lista_de_cadernos_tipo_dia:
                    if os.path.getsize(os.path.join('L:\\', 'rotina', ano, mes, dia, 'cadernos','{caderno}.dia'.format(caderno=cadeno_dia))) == 0:
                        self.lista_de_divergencia.append(cadeno_dia)
                
                for caderno_pdf in self.lista_de_cadernos_tipo_pdf:
                    if caderno_pdf not in self.lista_de_cadernos_tipo_dia:
                        self.lista_de_divergencia.append(caderno_pdf)
            except:
                print 'Acho que não temos dados nas pasta {pasta1} ou {pasta2}'.format(pasta1=pasta_de_rotina,pasta2=pasta_de_cadernos_preparados)

            self.printar_na_box(event= event, texto='\nCadernos com divergência de PDF com diário preparado ou tamanho zerado:\n')
            self.printar_na_box(event= event, texto=','.join(self.lista_de_divergencia))
        dlg_pronto = wx.MessageDialog(None , "Pronto, conferência feita.","Fim da conferencia.", wx.OK| wx.ICON_INFORMATION) 
        dlg_pronto.ShowModal()

class UI_conferidor_baixacao(Thread,object):
    """docstring for UI_conferidor_baixacao"""
    def __init__(self, arg):
        super(UI_conferidor_baixacao, self).__init__()
        self.frame = wx.Frame(None, -1, 'Buscar dados de confrencia de baixação', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,800,300)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.statusbar = self.frame.CreateStatusBar(1)

        wx.StaticBox(self.panel, wx.ID_ANY, 'PDF', (10, 5), size=(280, 110))
        
        self.texto_da_box_caderno = wx.StaticText(self.panel, wx.ID_ANY, "Digite o caderno:", (20, 20))
        self.box_caderno = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 35),size=(150, -1),style=wx.TE_PROCESS_ENTER)
        self.box_caderno.Bind(wx.EVT_TEXT_ENTER, self.abrir_pdf)

        self.texto_calendario = wx.StaticText(self.panel, wx.ID_ANY, "Data:", (25, 65))
        self.calendario = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 85),style=wx.DP_DROPDOWN)

        self.button_abrir_pdf = wx.Button(self.panel, wx.ID_ANY, 'Conferir', (200, 35)) 
        self.button_abrir_pdf.Bind(wx.EVT_BUTTON, self.abrir_pdf)

        wx.StaticBox(self.panel, wx.ID_ANY, 'NNX', (10, 125), size=(730, 120))
        
        self.texto_box_linha_inicial = wx.StaticText(self.panel, wx.ID_ANY, "Linha inicial:", (25, 145))
        self.texto_box_linha_inicial = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 160),size=(700, -1),style=wx.TE_READONLY)
        
        self.texto_box_linha_final = wx.StaticText(self.panel, wx.ID_ANY, "Linha final:", (25, 185))
        self.texto_box_linha_final = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 210),size=(700, -1),style=wx.TE_READONLY)
        
        self.frame.Show()
        self.frame.Centre()

    def abrir_pdf(self,event):
        data = self.calendario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        dia,mes,ano = data_ajustada.strftime('%d'),data_ajustada.strftime('%m'),data_ajustada.strftime('%Y')
        caderno = self.box_caderno.GetLineText(0).upper()
        caminho_da_pasta_do_nnx = os.path.join('L:\\', 'rotina', ano, mes, dia, 'download')
        caminho_da_pasta_do_pdf = os.path.join('L:\\', 'rotina', ano, mes, dia, 'download', caderno, 'X.pdf')
        try:
            self.statusbar.SetStatusText('Abrindo: {pasta}'.format(pasta=caminho_da_pasta_do_pdf))
            os.startfile(caminho_da_pasta_do_pdf)
            self.box_caderno.SetValue('')
            time.sleep(1)
            self.statusbar.SetStatusText('')
        
            with open('{pasta}\\{caderno}.NNX'.format(pasta=caminho_da_pasta_do_nnx,caderno=caderno), 'r') as arq_nnx:
                linhas = arq_nnx.readlines()
                self.texto_box_linha_inicial.SetValue(linhas[0])
                self.texto_box_linha_final.SetValue(linhas[-2])
                arq_nnx.close()
        except:
            self.statusbar.SetStatusText('Acho que não temos dados para {caderno}'.format(caderno=caderno))

class UI_DIV(Thread,object):
    """docstring for UI_DIV"""
    def __init__(self, arg):
        super(UI_DIV, self).__init__()
        self.frame = wx.Frame(None, -1, 'DIV', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,300,650)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.lista_do_saga = []
        self.lista_de_esferas = []
        self.tipo_de_lista = None        
        self.sinal_verde = None

        wx.StaticBox(self.panel, wx.ID_ANY, 'Esferas', (5, 5), size=(250, 125))

        wx.StaticBox(self.panel, wx.ID_ANY, 'Tipo de caderno', (5, 135), size=(250, 50))

        self.checkbox_conferencia =  wx.CheckBox(self.panel, wx.ID_ANY, "Conferência", (150, 50))
        
        self.checkbox_marcar_todas_as_esferas =  wx.CheckBox(self.panel, wx.ID_ANY, "Marcar tudo", (150, 25))
        self.checkbox_marcar_todas_as_esferas.Bind(wx.EVT_CHECKBOX,self.marca_todas_as_esferas)

        self.checkbox_esfera_federal =  wx.CheckBox(self.panel, wx.ID_ANY, "Esfera Federal", (25, 25))
        self.checkbox_esfera_federal.Bind(wx.EVT_CHECKBOX,self.validar_checkboxs)

        self.checkbox_esfera_trabalhista =  wx.CheckBox(self.panel, wx.ID_ANY, "Esfera Trabalhista", (25, 50))
        self.checkbox_esfera_trabalhista.Bind(wx.EVT_CHECKBOX,self.validar_checkboxs)

        self.checkbox_esfera_estadual =  wx.CheckBox(self.panel, wx.ID_ANY, "Esfera Estadual", (25, 75))
        self.checkbox_esfera_estadual.Bind(wx.EVT_CHECKBOX,self.validar_checkboxs)

        self.checkbox_esfera_superior =  wx.CheckBox(self.panel, wx.ID_ANY, "Esfera Superior", (25, 100))
        self.checkbox_esfera_superior.Bind(wx.EVT_CHECKBOX,self.validar_checkboxs)
        
        
        self.checkbox_lido_e_nao_feito =  wx.CheckBox(self.panel, wx.ID_ANY,  "Lido e não feito.", (25, 160))
        self.checkbox_nao_lido =  wx.CheckBox(self.panel, wx.ID_ANY, "não lido.", (150, 160))
        
        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data inicial:", (25, 200))
        self.calendario_inicial = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 225),style=wx.DP_DROPDOWN)
        

        self.texto_calendario_final = wx.StaticText(self.panel, wx.ID_ANY, "Data final:", (150, 200))
        self.calendario_final = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (150, 225),style=wx.DP_DROPDOWN)
                
        self.checkbox_conjunto =  wx.CheckBox(self.panel, wx.ID_ANY,  "Conjuntos:", (25, 265))
        self.checkbox_conjunto.Bind(wx.EVT_CHECKBOX,self.habilitar_box_conjunto)
        
        
        self.box_conjunto = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 290),size=(200,-1))
        self.box_conjunto.Enable(False)

        self.button_verificar = wx.Button(self.panel, wx.ID_ANY, 'Verifica', (20, 320))
        self.button_verificar.Bind(wx.EVT_BUTTON, self.vericar_no_pco)
        
        self.box_para_print = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 350),size=(230, 250),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)
        

        self.frame.Show()
        self.frame.Centre()
    
    def criar_lista_da_estrada_do_usuario(self,event):
        if self.box_conjunto.GetLineText(0) != '':
            return self.box_conjunto.GetLineText(0).split(' ')
        else:
            dlg_box_nome_do_novo_pdf = wx.MessageDialog(None , "Digite ao menos um conjunto.","Ops...", wx.OK| wx.ICON_QUESTION) 
            dlg_box_nome_do_novo_pdf.ShowModal()
    
    
    def habilitar_box_conjunto (self,event):
        if self.checkbox_conjunto.Value == False:
            self.box_conjunto.Enable(False)
            self.box_conjunto.SetValue("")
            self.sinal_verde = True
            self.tipo_de_lista = None  
        else:
            self.box_conjunto.Enable(True)
            self.tipo_de_lista = 'ENTRADA_DE_DO_USUARIO'
            self.sinal_verde = True
    
    
    
    def marca_todas_as_esferas (self,event):
        if self.checkbox_marcar_todas_as_esferas.Value == True:  
            self.checkbox_esfera_federal.SetValue(True)
            self.checkbox_esfera_trabalhista.SetValue(True)
            self.checkbox_esfera_estadual.SetValue(True)
            self.checkbox_esfera_superior.SetValue(True)
            self.checkbox_lido_e_nao_feito.SetValue(True)
            self.checkbox_nao_lido.SetValue(True)
       
        if self.checkbox_marcar_todas_as_esferas.Value == False:
            self.checkbox_esfera_federal.SetValue(False)
            self.checkbox_esfera_trabalhista.SetValue(False)
            self.checkbox_esfera_estadual.SetValue(False)
            self.checkbox_esfera_superior.SetValue(False)
            self.checkbox_lido_e_nao_feito.SetValue(False)
            self.checkbox_nao_lido.SetValue(False) 
    
    def buscar_nomes_nos_relatorios(self,event,pasta,cadernos,nomes):
        lista_de_cadernos_feitos_ou_vazios = []
        

        for caderno in cadernos:
            conferido = False
            with open('{pasta}\\{caderno}.rel'.format(pasta=pasta,caderno=caderno), 'r') as arq_rel:
                linhas = arq_rel.readlines()
                for linha in linhas:
                    nomes_buscados = '|'.join(nomes)
                    linha_com_nome = re.search(r'^V'+'({})$'.format(nomes_buscados), linha) 
                    linha_com_nome_de_conferencia = re.search(r'^sV'+'({})$'.format(nomes_buscados), linha)
                    caderno_vazio = re.search(r'^sb\.', linha)
                    if linha_com_nome or caderno_vazio:
                        lista_de_cadernos_feitos_ou_vazios.append(caderno.upper())
                        
                    if caderno_vazio:
                        conferido = True
                    if linha_com_nome_de_conferencia:
                        conferido = True
                       
            
            
            if caderno in self.lista_do_saga and conferido == False and self.checkbox_conferencia.Value == True:
                self.printar_na_box(event= event, texto='Caderno não conferido: {caderno}\n'.format(caderno=caderno))     
            else:
                pass
            
            arq_rel.close()
               
        
        return lista_de_cadernos_feitos_ou_vazios   
    
    
    
    
    def criar_lista_de_nomes_de_funcinarios(self,event):
        nomes = [
                'ubiratan',
                'fabio',
                'anisio',
                'miceli',
                'jessica',
                'fernanda',
                'helcio',
                'diegog',
                'fabricio',
                'fagner',
                'flavia', 
                'giselia', 
                'joao', 
                'julio', 
                'leandro', 
                'mario', 
                'renata', 
                'ricardo',
                'wesley', 
                'yan',]
        return nomes 
    
    def criar_relatorio_txt(self,event,caderno,conjunto,dia,mes,ano,status):
        with open((os.path.join(os.environ['USERPROFILE'], 'Desktop','Relatorio_DIV','{dia}-{mes}-{ano}-relatorio.txt'.format(dia=dia,mes=mes,ano=ano))), 'a+t') as arq_txt:
                linhas = arq_txt.readlines()
                
                linha_da_data = '{dia}/{mes}/{ano}\n'.format(dia=dia,mes=mes,ano=ano)
                if linha_da_data not in linhas:
                    arq_txt.write(linha_da_data)
                
                linha_do_conjunto = '######Conjunto###### {conjunto}\n'.format(conjunto=conjunto)
                if linha_do_conjunto not in linhas:
                    arq_txt.write('\n')
                    arq_txt.write(linha_do_conjunto)
                
                linha_do_caderno = '{status} {caderno}\n'.format(status=status,caderno=caderno)
                arq_txt.write(linha_do_caderno)

    
    def mostar_lista_de_cadernos_preparados(self,event,pasta_de_preparados):
        lista_de_cadernos_dia = []
        pasta_de_cadernos_pre = pasta_de_preparados
        lista_de_aquivos_dia = os.listdir(pasta_de_cadernos_pre)
        for arquivo in lista_de_aquivos_dia:
            arquivo_dia = re.search(r'^(.*)\.(dia|DIA)', arquivo)
            if arquivo_dia:
                lista_de_cadernos_dia.append(arquivo_dia.group(1).upper())

        return sorted(lista_de_cadernos_dia)
   
    def formar_pasta_de_cadernos(self,event,dia,mes,ano):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'cadernos')
    
    def formar_pasta_de_rel(self,event,conjunto,dia,mes,ano):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'dados', '1_{conjunto}'.format(conjunto=conjunto), 'rel')
    
    def definir_conjuntos(self,event,pasta):
        lista_de_conjuntos = []
        try:
            pastas = os.listdir(pasta)
            for pasta in pastas:
                conjunto = re.search(r'^(1_)([0-9]{1,})', pasta)
                if conjunto:       
                    lista_de_conjuntos.append(conjunto.group(2))

            self.sinal_verde = True
            return sorted(lista_de_conjuntos)
        except:
            self.sinal_verde = False 
            
    def mostar_lista_de_cadernos_lidos(self,event,pasta_de_relatorios):
        lista_de_cadernos = []
        pasta = pasta_de_relatorios
        lista_de_aquivos = os.listdir(pasta)
        for arquivo in lista_de_aquivos:
            caderno = re.search(r'^(.*)\.rel', arquivo).group(1)
            lista_de_cadernos.append(caderno.upper())

        return sorted(lista_de_cadernos)
    
    
    
    def validar_checkboxs(self,event):
        self.lista_de_esferas = []

        if self.checkbox_esfera_federal.Value == True:
            self.lista_de_esferas.append('FED')    
        
        if self.checkbox_esfera_trabalhista.Value == True:
            self.lista_de_esferas.append('TRAB')  
        
        if self.checkbox_esfera_estadual.Value == True:
            self.lista_de_esferas.append('EST')  
        
        if self.checkbox_esfera_superior.Value == True:
            self.lista_de_esferas.append('SUP')  
        
        if self.checkbox_marcar_todas_as_esferas.Value == True:
            self.lista_de_esferas = []
            self.lista_de_esferas.append('')
    
        
    def calcular_intervalo_de_datas(self,event,data_inicial,data_final):
        dif_de_datas = []
        if data_inicial == data_final:
            dif_de_datas.append(data_inicial)
        if data_inicial != data_final:  
            dif_de_datas.append(data_inicial)
            while data_final > data_inicial:
                data_inicial = data_inicial.fromordinal(data_inicial.toordinal()+1)
                dif_de_datas.append(data_inicial)
        
        return dif_de_datas   

    
    def gera_data(self,event,caledario):
        data = caledario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data_ajustada

    def criar_dia_mes_ano(self,event,data):
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')

    
    def printar_na_box(self, event,texto):
        self.box_para_print.AppendText(texto)

    
    def formar_pasta_de_dados(self,event,dia,mes,ano):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'dados')
    
    
    def formar_lista_de_cadernos_do_saga(self,event,esferas):
        lista_de_cadernos = []

        for esfera in esferas:
            sessao_lido = sessionmaker(bind=db_sys_engine)()
            q_cadernos = sessao_lido.query(Caderno)
            if esfera:
                q_cadernos = q_cadernos.filter(Caderno.esfera == esfera.decode('latin-1'))
            for caderno in q_cadernos.all():
                lista_de_cadernos.append(caderno.nome)
            
            sessao_lido.close()

        return lista_de_cadernos

    def criar_lista_do_pco(self,event,conjunto):
        
        parceira_id = 1
        
        session = Session()
        query_clientes = session.query(sm.Cliente)
        query_clientes = query_clientes.filter(sm.Cliente.conjunto==conjunto)
        query_clientes = query_clientes.join(sm.Parceira.clientes)
        query_clientes = query_clientes.filter(sm.Parceira.id==parceira_id)
        ids_clientes_ativos = [c.id for c in query_clientes.all() if c.ativo]
        #
        query_cadernos = session.query(sm.Caderno.nome)
        query_cadernos = query_cadernos.join(sm.Cliente.grupos, sm.Grupo.pesquisas, sm.Pesquisa.pacotes, sm.Pacote.cadernos)
        query_cadernos = query_cadernos.filter(sm.Cliente.id.in_(ids_clientes_ativos))
        query_cadernos = query_cadernos.group_by(sm.Caderno.nome)
        #print(list(sorted([x[0] for x in query_cadernos.all()])))
        return list(sorted([x[0] for x in query_cadernos.all()]))
    
            

    def vericar_no_pco(self,event):
        self.box_para_print.SetValue('')
        self.validar_checkboxs(None)
        self.lista_do_saga = self.formar_lista_de_cadernos_do_saga(event=event,esferas=self.lista_de_esferas)
        data_inicial = self.gera_data(event = event, caledario = self.calendario_inicial)
        data_final = self.gera_data(event = event, caledario = self.calendario_final)
        
        dia_inicial,mes_inicial,ano_inicial = self.criar_dia_mes_ano(event= event, data = data_inicial)
        
        self.printar_na_box(event= event, texto='Data inicial: ')
        self.printar_na_box(event= event, texto='{dia}/{mes}/{ano}\n'.format(dia=dia_inicial,mes=mes_inicial,ano=ano_inicial))
        if data_final != data_inicial: 
            self.printar_na_box(event= event, texto='Data final: ')
            dia_final,mes_final,ano_final = self.criar_dia_mes_ano(event= event, data = data_final)
            self.printar_na_box(event= event, texto='{dia}/{mes}/{ano}\n'.format(dia=dia_final,mes=mes_final,ano=ano_final))
            datas = self.calcular_intervalo_de_datas(event = event, data_inicial = data_inicial, data_final = data_final)
        else:
            datas = [data_inicial]

        self.printar_na_box(event= event, texto='\n---------------------------------------------\n')
        

        for data in datas:
            
            dia,mes,ano = self.criar_dia_mes_ano(event= event, data = data)
            
            self.printar_na_box(event= event, texto='\n')
            self.printar_na_box(event= event, texto='\nData: {dia}/{mes}/{ano}\n'.format(dia=dia,mes=mes,ano=ano))
            pasta_de_dados = self.formar_pasta_de_dados(event = event, dia = dia, mes = mes, ano = ano)
            if self.tipo_de_lista == 'ENTRADA_DE_DO_USUARIO':
                lista_de_conjuntos = self.criar_lista_da_estrada_do_usuario(None)
            else:    
                lista_de_conjuntos = self.definir_conjuntos(event = event ,pasta=pasta_de_dados)
            
            if self.checkbox_lido_e_nao_feito.Value == False and self.checkbox_nao_lido.Value == False:
                dlg_box_checkbox_lido = wx.MessageDialog(None , "Sem uma opção do que tenho que fazer fico em dúvida.","Ops...", wx.OK| wx.ICON_QUESTION) 
                dlg_box_checkbox_lido.ShowModal()
                self.sinal_verde = False
            
            if self.sinal_verde == True:
                lista_de_nomes = self.criar_lista_de_nomes_de_funcinarios(None)
                
                max = len(lista_de_conjuntos)
                count = 0
                dlg_carregar = wx.ProgressDialog("Processando", "Tempo estimado", max, parent=self.frame ,style= wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
               
                for conjunto in lista_de_conjuntos:
                    count = count + 1
                    if count < max:
                        dlg_carregar.Update(count)
                    else:
                        dlg_carregar.Update(False)
                    
                    self.printar_na_box(event= event, texto='\n')
                    self.printar_na_box(event= event, texto='\n'+'-----------Conjunto {conjunto}-----------\n'.format(conjunto=conjunto))

                    try:
                        caminho_da_pasta_de_relatorios = self.formar_pasta_de_rel(event=event,conjunto=conjunto,dia=dia,mes=mes,ano=ano)
                        lista_de_cadernos_lidos_do_conjunto = self.mostar_lista_de_cadernos_lidos(event=event, pasta_de_relatorios=caminho_da_pasta_de_relatorios)
                        lista_de_cadernos_feitos_ou_vazios = self.buscar_nomes_nos_relatorios(event=event,pasta=caminho_da_pasta_de_relatorios,cadernos=lista_de_cadernos_lidos_do_conjunto,nomes=lista_de_nomes)
                        resultado = set(lista_de_cadernos_lidos_do_conjunto)
                        resultado2 = set(lista_de_cadernos_feitos_ou_vazios)

                        if self.checkbox_lido_e_nao_feito.Value == True: 
                            
                            self.printar_na_box(event= event, texto='\nCadernos que foram lidos e não feitos: ')
                            c = list(resultado.symmetric_difference(resultado2))
                            for result_lidoXrel in sorted(c):
                                self.criar_relatorio_txt(event=event,caderno=result_lidoXrel,conjunto=conjunto,dia=dia,mes=mes,ano=ano,status='Lidos e não feitos:')
                                if result_lidoXrel in self.lista_do_saga:
                                    self.printar_na_box(event= event, texto='\n{}'.format(result_lidoXrel))
                        
                        if self.checkbox_nao_lido.Value == True:
                            
                            
                            pasta_de_arq_de_cadernos_pre =  self.formar_pasta_de_cadernos(event=event,dia=dia,mes=mes,ano=ano)
                            lista_de_cadernos_preparados = self.mostar_lista_de_cadernos_preparados(event=event,pasta_de_preparados=pasta_de_arq_de_cadernos_pre)

                            try:
                                cadernos_pco = self.criar_lista_do_pco(event=event,conjunto=conjunto)
                                        
                                for caderno_rel in lista_de_cadernos_feitos_ou_vazios:
                                    
                                    if caderno_rel not in cadernos_pco:
                                        cadernos_pco.append(caderno_rel)

                                lista_banco = []
                                cadernos_pco = set(cadernos_pco)
                                lista_arq_dia = set(lista_de_cadernos_preparados)
                                result_diaXbanco = (lista_arq_dia).intersection(cadernos_pco)
                                for dados_diaXbanco in sorted(result_diaXbanco):
                                    if dados_diaXbanco not in lista_banco:
                                        lista_banco.append(dados_diaXbanco)

                                lista_banco = set(lista_banco)
                                            
                                result_bancoXrel = (lista_banco.symmetric_difference(resultado))
                                self.printar_na_box(event= event, texto='\n'+'Cadernos preparados e não feitos: ')
                                for dados_bancoXrel in sorted(result_bancoXrel):
                                    self.criar_relatorio_txt(event=event,caderno=dados_bancoXrel,conjunto=conjunto,dia=dia,mes=mes,ano=ano,status='Preparados e não feitos:')
                                    if dados_bancoXrel in self.lista_do_saga:
                                        self.printar_na_box(event= event, texto='\n{}'.format(dados_bancoXrel))            
                                            
                            except:
                                self.printar_na_box(event= event, texto='\n\nO cliente provavelmente era de teste\n e/ou não deve estar na nossa base \nde dados para esse conjunto nesse dia.')
                                continue    
                    except:
                        self.printar_na_box(event= event, texto='\n\nProvavelmente não temos leitura \nde cadernos para esse dia.')
                
                dlg_carregar.Destroy()            


            else:
                self.printar_na_box(event= event, texto="\nAcho que não temos dados para essa.\n Data: {dia}/{mes}/{ano}".format(dia=dia,mes=mes,ano=ano))
                self.printar_na_box(event= event, texto='\n#######################\n')
    
                           
        
        dlg_pronto = wx.MessageDialog(None , "Pronto, Conferência feita.","Fim da conferencia.", wx.OK| wx.ICON_INFORMATION) 
        dlg_pronto.ShowModal()  

class UI_abrir_pdf(Thread,object):
    """docstring for UI_abrir_pdf"""
    def __init__(self, arg):
        super(UI_abrir_pdf, self).__init__()
        self.frame = wx.Frame(None, -1, 'Abri PDF', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,300,200)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        
        self.statusbar = self.frame.CreateStatusBar(1)
        
        
        
        self.texto_da_box_caderno = wx.StaticText(self.panel, wx.ID_ANY, "Digite o caderno:", (20, 15))
        self.box_caderno = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 35),size=(150, -1),style=wx.TE_PROCESS_ENTER)
        self.box_caderno.Bind(wx.EVT_TEXT_ENTER, self.abrir_pdf)

        self.texto_calendario = wx.StaticText(self.panel, wx.ID_ANY, "Data:", (25, 75))
        self.calendario = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 100),style=wx.DP_DROPDOWN)

        self.button_abrir_pdf = wx.Button(self.panel, wx.ID_ANY, 'Abrir PDF', (200, 35)) 
        self.button_abrir_pdf.Bind(wx.EVT_BUTTON, self.abrir_pdf)

        
        self.frame.Show()
        self.frame.Centre()

    def abrir_pdf(self,event):
        data = self.calendario.GetValue()
        data_ajustada = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        dia,mes,ano = data_ajustada.strftime('%d'),data_ajustada.strftime('%m'),data_ajustada.strftime('%Y')
        caderno = self.box_caderno.GetLineText(0).upper()
        caminho_da_pasta_do_pdf = os.path.join('L:\\', 'rotina', ano, mes, dia, 'download', caderno, 'X.pdf')
        try:
            self.statusbar.SetStatusText('{pasta}'.format(pasta=caminho_da_pasta_do_pdf))
            os.startfile(caminho_da_pasta_do_pdf)
            self.box_caderno.SetValue('')
            time.sleep(1)
            self.statusbar.SetStatusText('')
        except:
           self.statusbar.SetStatusText('Acho que não temos dados para {pasta}'.format(pasta=caminho_da_pasta_do_pdf)) 

class UI_BAIXADOR(Thread,object):
    """docstring for UI_BAIXADOR"""
    def __init__(self, arg):
        super(UI_BAIXADOR, self).__init__()
        self.frame = wx.Frame(None, -1, 'Baixador', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,300,125)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        
        self.statusbar = self.frame.CreateStatusBar(1)
        
        self.dic_sites = {
            'AMMU1': 'http://www.diariomunicipal.com.br/aam',
            'ALMU1': 'http://www.diariomunicipal.com.br/ama',
            'CEMU1': 'http://www.diariomunicipal.com.br/aprece',
            'GOMU1': 'http://www.diariomunicipal.com.br/agm',
            'GOMU2': 'http://www.diariomunicipal.com.br/fgm',
            'PAMU1': 'http://www.diariomunicipal.com.br/famep',
            'PIMU1': 'http://www.diariomunicipal.com.br/appm',
            'RJMU2': 'http://www.diariomunicipal.com.br/aemerj',
            'RRMU1': 'http://www.diariomunicipal.com.br/amr',
            'ROMU1': 'http://www.diariomunicipal.com.br/arom',
            'SPMU2': 'http://www.diariomunicipal.com.br/apm',
            'MACATUBAMU1': 'http://www.diariomunicipal.com.br/macatuba',
            'MSMU1':'http://www.diariomunicipal.com.br/assomasul',
            'RNMU1':'http://www.diariomunicipal.com.br/femurn',
            'PBMU1':'http://www.diariomunicipal.com.br/famup',
            'PEMU1':'http://www.diariomunicipal.com.br/amupe',
            'PBMU1':'http://www.diariomunicipal.com.br/famup',
            'MGMU1':'http://www.diariomunicipal.com.br/amm-mg',
            'PRMU1':'http://www.diariomunicipal.com.br/amp',
            'RSMU1':'http://www.diariomunicipal.com.br/famurs',
            'TESTE':'https://www.globo.com/',
            'FERIADOS3': 'http://www.feriados.com.br/',
            'FERIADOS2': 'http://pt.wikipedia.org/wiki/Feriados_no_Brasil',
            'FERIADOS1': 'http://www.feriadosmunicipais.com.br/',
            'FERIADOS':'http://www.feriados.com.br/feriados-porto_alegre-rs.php',
            'VREDONDAMU1': 'http://new.voltaredonda.rj.gov.br/vrdestaque/',
            'VTCMU1': 'http://dom.pmvc.ba.gov.br/',
            'VITORIAESMU1': 'http://diariooficial.vitoria.es.gov.br/',
            'VVELHAMU1': 'http://www.vilavelha.es.gov.br/diariooficial/',
            'UBERABAMU1': 'http://www.uberaba.mg.gov.br/portal/conteudo,10453',
            'TCSPMU1': 'http://www.imprensaoficial.com.br/',
            'TCRJMU1': 'http://doweb.rio.rj.gov.br/',
            'TCUN3': 'http://portal.in.gov.br/',
            'TCUBOLETIM': 'https://portal.tcu.gov.br/transparencia/btcu/',
            'TCUN2': 'http://portal.in.gov.br/',
            'TCUN1': 'http://portal.in.gov.br/',
            'TCTO1': 'https://www.tce.to.gov.br/sitetce/',
            'TCSP1': 'http://www.imprensaoficial.com.br/PortalIO/Home_1_0.aspx#08/08/2009',
            'TCSE1': 'https://www.tce.se.gov.br/diarioeletronico/integra/integrainternetform.aspx',
            'TCSC1': 'http://www.tce.sc.gov.br/diario-oficial',
            'TCRS1': 'http://www2.tce.rs.gov.br/portal/page/portal/tcers/',
            'TCRO1': 'http://www.tce.ro.gov.br/',
            'TCRN1': 'http://www.tce.rn.gov.br/',
            'TCRJ1': 'http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_data.php',
            'TCPR1A': 'http://www1.tce.pr.gov.br/',
            'TCPR1': 'http://www1.tce.pr.gov.br/',
            'TCPI1': 'https://www.tce.pi.gov.br/cidadao/diario-oficial/',
            'TCPE1': 'http://www4.tce.pe.gov.br/internet/',
            'TCPB1': 'https://portal.tce.pb.gov.br/',
            'TCMT1': 'http://www.tce.mt.gov.br/diario/index',
            'TCMS1': 'http://www.tce.ms.gov.br/diarios',
            'TCMG1': 'http://www.tce.mg.gov.br/#',
            'TCMBE': 'http://www.tcm.pa.gov.br/',
            'TCMBA': 'http://localhost/alerte_bc/baixador.php?action=principal',
            'TCMA1': 'http://site.tce.ma.gov.br/',
            'TCGO1':  'http://dec.tce.go.gov.br/',
            'TCES1': 'http://diario.tce.es.gov.br//',
            'TCERS': 'http://www.tce.rs.gov.br/',
            'TCCE1': 'https://www.tce.ce.gov.br/diario-oficial/consulta-por-data-de-edicao',
            'TCBA1': 'http://www.tce.ba.gov.br/',
            'TCAP1': 'http://www.tce.ap.gov.br/diario-oficial',
            'TCAM1': 'http://doe.tce.am.gov.br/',
            'TCAL1': 'http://www.tce.al.gov.br/',
            'TCAC1': 'http://www.tce.ac.gov.br/',
            'TRF5SI': 'https://www.trf5.jus.br/',
            'TRF5INT': 'https://www4.trf5.jus.br/intimacoesEletronicas',
            'TRF4SI': 'http://www2.trf4.jus.br/trf4/',
            'TRF4I': 'http://www2.trf4.jus.br/trf4/',
            'TRF3SI': 'http://www.trf3.jus.br/',
            'TRF3II': 'http://www.trf3.jus.br/',
            'TRF3I': 'http://www.trf3.jus.br/',
            'TRF2SI': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx',
            'TRF2AX': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx',
            'TRF2A': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx',
            'TRF1INT': 'http://portal.trf1.jus.br/intimacoes/',
            'TOTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'TOTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'TOJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'TODJ': 'http://www.tjto.jus.br/',
            'MPTO': 'https://www.mpto.mp.br/web/portal/',
            'TJPEINT': 'http://www.tjpe.jus.br/web/intimacoes-pje',
            'TERESINAMU1': 'http://dom.teresina.pi.gov.br',
            'TAUBATEMU1': 'http://www.taubate.sp.gov.br/',
            'SUZANOMU1': 'http://www.suzano.sp.gov.br/web/transparencia/imprensa-oficial/',
            'SLUIZMU1': 'http://sistemas.semad.saoluis.ma.gov.br:8090/easysearch/',
            'SJMERITIMU1': 'http://www.meriti.rj.gov.br/diario-oficial-municipal-digital/',
            'SUMAREMU1': 'http://www.sumare.sp.gov.br/',
            'SALVADORMU1': 'http://www.salvador.ba.gov.br/',
            'SPJC': 'https://www.imprensaoficial.com.br/#',
            'SPLEG': 'http://www.imprensaoficial.com.br/PortalIO/Home_1_0.aspx#08/08/2009',
            'SPOAB1': 'http://www.oabsp.org.br/noticias/2013/09/20/Comunicado_Diario%20Oficial_13-09.jpg/view',
            'SPCAD5': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD4P3': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD4P2': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD4': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD3': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD2SI': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD2': 'ftp://ftp.tj.sp.gov.br/',
            'SPCAD1': 'ftp://ftp.tj.sp.gov.br/',
            'TJSP': 'ftp://ftp.tj.sp.gov.br/',
            'TRF5SI': 'https://www.trf5.jus.br/',
            'TRF5INT': 'https://www.trf5.jus.br/',
            'TRF5I': 'https://www.trf5.jus.br/',
            'TRF1SI': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'TRF1A': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'TITSP': 'https://www.fazenda.sp.gov.br/pauta/pages/ConsultaPauta.aspx',
            'TITPAUTA': 'https://www.fazenda.sp.gov.br/pauta/pages/ConsultaPauta.aspx',
            'SUMAREMU1': 'http://www.sumare.sp.gov.br/',
            'SULJF': 'http://www2.trf4.jus.br/trf4/',
            'SPTRT2': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'SPTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'SPTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'SPMU1X': 'http://www.imprensaoficial.com.br/',
            'SPMU1': 'http://www.imprensaoficial.com.br/',
            'SPMP': 'http://www.mp.sp.gov.br/portal/page/portal/DO_Estado',
            'SPJM1': 'http://www.tjmsp.jus.br/',
            'SPCADS': 'https://www.dje.tjsp.jus.br/cdje/index.do',
            'SPAD': 'http://aplicacoes1.trtsp.jus.br/ConsultaDOE/',
            'SPC5': 'http://aplicacoes1.trtsp.jus.br/ConsultaDOE/',
            'SPE3': 'https://www.fazenda.sp.gov.br/DiarioEletronico/ConsultaPublica.aspx',
            'SPE2': 'http://www.imprensaoficial.com.br',
            'SPE1': 'http://www.imprensaoficial.com.br',       
            'SOROCABAMU1': 'http://agencia.sorocaba.sp.gov.br/jornal-do-municipio/',
            'SJDOSPINHAISMU1': 'http://www.diariooficial.sjp.pr.gov.br/',
            'SJDOSCAMPOSMU1': 'http://servicos2.sjc.sp.gov.br/servicos/portal_da_transparencia/boletim_municipio.aspx',
            'SJMERITIMU1': 'http://www.meriti.rj.gov.br//',
            'SETELAGOASMU1' :'http://diario.setelagoas.mg.gov.br/',
            'SENADO1': 'http://legis.senado.gov.br/diarios/PublicacoesOficiais',
            'SEFSE': 'http://www.sefaz.se.gov.br/conteudo/46',
            'SEFSC': 'http://www.sef.sc.gov.br/',
            'SEFPB': 'https://www.receita.pb.gov.br/ser/servirtual/2016-01-05-19-01-00',  
            'SEFMG': 'http://diarioeletronicoccmg.fazenda.mg.gov.br/',
            'SEFAM': 'http://www.sefaz.am.gov.br/',
            'SETRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'SEJF': 'https://www.trf5.jus.br/',
            'SETRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'SEDJ': 'http://www.tjse.jus.br/portal/',
            'SDEPARNAIBAMU1': 'http://www.santanadeparnaiba.sp.gov.br/',
            'SCTRT2': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'SCTRT': 'http://www.trt12.jus.br/doe/publicacoessimplescon.do?evento=x',
            'SCTRE1A': 'http://www.tse.gov.br/internet/index.html',
            'SCTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'SCLEG': 'http://www.alesc.sc.gov.br/portal/diarios/indexdiario.php#',
            'SCMULIC': 'https://www.diariomunicipal.sc.gov.br/site/',
            'SCDJA': 'http://www.tj.sc.gov.br/imagens/ico_diariojustica',
            'SCDJ': 'http://app.tjsc.jus.br/consultadje/consulta.action',
            'SCDJSI': 'http://www.tj.sc.gov.br/imagens/ico_diariojustica',
            'SBCAMPOMU1': 'http://www.saobernardo.sp.gov.br/imprensa-oficial',  
            'SANTOSMU1': 'http://www.santos.sp.gov.br/', 
            'SANTOANDREMU1': 'http://www2.santoandre.sp.gov.br/',
            'SANTANADOPARNAIBA': 'http://www.santanadeparnaiba.sp.gov.br/',
            'RSAD': 'http://www.tjrs.jus.br/',
            'RSMU1': 'http://www.diariomunicipal.com.br/famurs/',
            'RSTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'RSTRE1': 'http://www.tre1-rs.jus.br/',
            'RSLEG': 'http://www.al.rs.gov.br/legislativo/DOAL.aspx',
            'RSDJ1SI': 'http://www.tjrs.jus.br/',
            'RSDJ4': 'http://www.tjrs.jus.br/',
            'RSDJ3': 'http://www.tjrs.jus.br/',
            'RSDJ2': 'http://www.tjrs.jus.br/',
            'RSDJ1': 'http://www.tjrs.jus.br/',
            'RRTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'RRTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'RRJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'RRDJ': 'http://diario.tjrr.jus.br/',
            'RPIS2': 'http://revistas.inpi.gov.br/rpi/',
            'RPIS1': 'http://revistas.inpi.gov.br/rpi/',
            'ROTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'ROTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'ROJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'RODJ': 'http://www.tjro.jus.br/',
            'RNMU1': 'http://www.diariomunicipal.com.br/femurn/',
            'RNTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'RNTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'RNJF': 'https://www.trf5.jus.br/',
            'RNDJ2': 'https://diario.tjrn.jus.br/djonline/inicial.jsf',
            'RNAD': 'https://diario.tjrn.jus.br/djonline/inicial.jsf',
            'RJTJA': 'https://www3.tjrj.jus.br/consultadje/',
            'RJTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'RJTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'RJP5': 'http://www.imprensaoficial.rj.gov.br/portal/modules/content/index.php?id=21',
            'RJMULIC': 'http://doweb.rio.rj.gov.br/',
            'RJMU1': 'http://doweb.rio.rj.gov.br/',
            'RJMP': 'https://www.mprj.mp.br/busca?p_p_id=mprjbusca_WAR_mprjbuscaportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_mprjbusca_WAR_mprjbuscaportlet_jspPage=%2Fhtml%2Fview.jsp&_mprjbusca_WAR_mprjbuscaportlet_exibicao_param=card&_mprjbusca_WAR_mprjbuscaportlet_filtro_param=doerj&_mprjbusca_WAR_mprjbuscaportlet_delta=15&_mprjbusca_WAR_mprjbuscaportlet_keywords=&_mprjbusca_WAR_mprjbuscaportlet_advancedSearch=false&_mprjbusca_WAR_mprjbuscaportlet_andOperator=true&_mprjbusca_WAR_mprjbuscaportlet_resetCur=false&_mprjbusca_WAR_mprjbuscaportlet_cur=1',
            'RJLEG': 'http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_data.php',
            'RJJFX': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx',
            'RJJF': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx',
            'RJJC': 'http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_data.php',
            'RJCAD5': 'http://www.adinp.com.br/',
            'RJCAD4': 'http://www.adinp.com.br/',
            'RJCAD3': 'http://www.adinp.com.br/',
            'RJCAD2SI': 'http://www.adinp.com.br/',
            'RJCAD2': 'http://www.adinp.com.br/',
            'RJCAD1': 'http://www.adinp.com.br/',
            'RJTJ': 'https://www3.tjrj.jus.br/consultadje/',
            'RECMU1': 'http://www.cepe.com.br/',
            'RJP5': 'http://www.imprensaoficial.rj.gov.br/portal/modules/content/index.php?id=21',
            'PRTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'PRTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'PRMU1': 'http://www.diariomunicipal.com.br/amp/',
            'PRLEG': 'https://www.documentos.dioe.pr.gov.br/dioe/consultaPublicaPDF.do?action=pgLocalizar&enviado=true&numero=&dataInicialEntrada=&dataFinalEntrada=&search=&diarioCodigo=3&submit=Localizar&localizador=',
            'PRDJ2X': 'http://www.tjpr.jus.br/arquivos-diario-da-justica',
            'PRDJ2SI': 'http://www.tjpr.jus.br/arquivos-diario-da-justica',
            'PRDJ2D': 'http://www.tjpr.jus.br/arquivos-diario-da-justica',
            'PRDJ2': 'http://www.tjpr.jus.br/arquivos-diario-da-justica',
            'PORTOVELHOMU1': 'http://www.diariomunicipal.com.br/arom/',
            'POAMU1': 'http://www2.portoalegre.rs.gov.br/portal_pmpa_novo/',
            'PIRACICABAMU1': 'http://www.piracicaba.sp.gov.br/diarios',
            'PIMP': 'http://aplicativos3.mppi.mp.br/consultadiariomp/publico/index.xhtml',
            'PITRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'PITRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'PIJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'PIDJ': 'http://www.tjpi.jus.br/site/Init.mtw',
            'PETROPOLISMU1': 'http://www.petropolis.rj.gov.br/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/235-2019.html',
            'PEMU1': 'http://www.diariomunicipal.com.br/amupe/',
            'PETRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'PETRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'PEMP': 'http://mppe.mp.br/mppe/index.php/sou-ministerio/diario-oficial-link-sou-mppe/category/650-diario-oficial-2019',
            'PELEG': 'http://www.alepe.pe.gov.br/',
            'PEJF': 'http://www.trf5.jus.br/',
            'PEDJ': 'https://www.tjpe.jus.br/dje',
            'EXPE1': 'http://www.cepe.com.br/templates/cepe/images/btAcessoDiario.png',
            'PBTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'PBTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'PBMU1': 'http://www.diariomunicipal.com.br/famup/',
            'PBJF': 'https://www.trf5.jus.br/',
            'PBDJ': 'https://app.tjpb.jus.br/dje/paginas/diario_justica/publico/buscas.jsf',
            'PALMASMU1': 'http://diariooficial.palmas.to.gov.br/',
            'PATRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'PATRE1': 'http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/',
            'PADO': 'http://www.ioepa.com.br/#2',
            'PAJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'PADJ': 'http://www.tjpa.jus.br/PortalExterno/',
            'OHOJE': 'http://ohoje.com/',
            'OABNAC': 'https://deoab.oab.org.br/pages/visualizacao',
            'NOVAFRIBURGOMU1': 'http://www.pmnf.rj.gov.br/',
            'NITEROIMU1': 'http://www.niteroi.rj.gov.br/',
            'NIGUACUMU1': 'http://www.novaiguacu.rj.gov.br/',
            'NATALMU1': 'https://natal.rn.gov.br/',
            'MTTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'MTTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'MTMU1': 'https://diariomunicipal.org/mt/amm/',
            'MTJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'MTDO': 'http://www.iomat.mt.gov.br',
            'MTDJ': 'http://www.tjmt.jus.br/dje',
            'MSTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'MSTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'MSMU1': 'http://www.diariomunicipal.com.br/assomasul',
            'MSMP': 'https://www.mpms.mp.br/domp',
            'MSLEG': 'http://diariooficial.al.ms.gov.br/',
            'MSDO': 'http://ww1.imprensaoficial.ms.gov.br/search/',
            'MSDJ': 'http://www.tjms.jus.br',
            'MPF1': 'http://www.transparencia.mpf.mp.br/',
            'MUNICIPIOSRJ': 'http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_data.php',
            'MUNICIPIOSAM': 'http://www.diariomunicipal.com.br/aam/',
            'MGFI': 'https://dje.tjmg.jus.br/ultimaEdicao.do', 
            'MGTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'MGTRT':'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'MGSISI': 'http://dje.tjmg.gov.br/apresentacao.do',
            'MGSI': 'http://dje.tjmg.gov.br/apresentacao.do',
            'MGMP': 'https://www.mpmg.mp.br/',
            'MGLEG': 'http://www.almg.gov.br/consulte/arquivo_diario_legislativo/',
            'MGMU1': 'http://www.diariomunicipal.com.br/amm-mg/',
            'MGJM1': 'http://www.tjmmg.jus.br/',
            'MGJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'MGFB': 'http://dje.tjmg.gov.br/ultimaEdicao.do',
            'MGED': 'http://www.tjmg.gov.br/',
            'MGAD': 'http://dje.tjmg.gov.br/ultimaEdicao.do',
            'MARILIAMU1': 'https://diariooficial.marilia.sp.gov.br/',
            'MACEIOMU1': 'http://www.maceio.al.gov.br/noticias/diario-oficial/',
            'MANAUSMU1': 'http://dom.manaus.am.gov.br/',
            'MAMU1': 'http://www.diariooficial.famem.org.br/dom/dom/todasEdicoes',
            'MATRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'MAJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'MADJ': 'http://www.tjma.jus.br/inicio/diario', 
            'MATRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'LDEFREITASMU1': 'http://io.org.br/ba/laurodefreitas/diarioOficial',
            'LEMEMU1': 'http://www.leme.sp.gov.br/imprensa',
            'LIMEIRAMU1': 'http://serv42.limeira.sp.gov.br/jof/NetJornal_cns_edicoes_cons_site/',
            'JUNDIAIMU1': 'http://imprensaoficial.jundiai.sp.gov.br/',
            'JPESSOAMU1': 'http://www.joaopessoa.pb.gov.br/semanariooficial/',
            'JFSEINT': 'https://www.trf5.jus.br/',
            'JFRNINT': 'https://www.trf5.jus.br/',
            'JFPEINT': 'https://www.trf5.jus.br/',
            'JFPBINT': 'https://www.trf5.jus.br/',
            'JFCEINT': 'https://www.trf5.jus.br/',
            'JFALINT': 'https://www.trf5.jus.br/',
            'JFORAMU1': 'https://www.pjf.mg.gov.br/e_atos/e_atos.php',
            'ITAQUAQUECETUBAMU1': 'https://www.itaquaquecetuba.sp.gov.br/diario-oficial/',
            'INDAIATUBAMU1': 'https://www.indaiatuba.sp.gov.br/comunicacao/imprensa-oficial/edicoes/',
            'IBAMED': 'http://www.ibama.gov.br/',
            'GUARATINGUETAMU1': 'http://guaratingueta.sp.gov.br/jornal-oficial-da-estancia-turistica-de-guaratingueta/',
            'GVALADARESMU1': 'http://www.valadares.mg.gov.br/diario-eletronico',
            'GRMU1': 'http://www.guarulhos.sp.gov.br/index.php?option=com_content&view=article&id=402&Itemid=57',
            'GOTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'GOTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'GOTCM': 'http://www.tcm.go.gov.br/portal/',
            'GOMP2': 'http://www.mpgo.mp.br/portal/domp',
            'GOMP': 'http://www.mpgo.mp.br/portal/domp',
            'GOLEG': 'https://portal.al.go.leg.br/transparencia/diario', 
            'GOJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'GOIMU1': 'http://www4.goiania.go.gov.br/portal/site.asp?s=775&m=2075',
            'GODJ2': 'http://www.tjgo.jus.br/',
            'GODJ': 'http://www.tjgo.jus.br/',
            'FORMU1': 'https://diariooficial.fortaleza.ce.gov.br/',
            'FLORIPAMU1': 'http://www.pmf.sc.gov.br/governo/index.php?pagina=govdiariooficial',
            'FERIADOS2': 'http://www.feriados.com.br/',
            'FERIADOS MUNICIPAIS': 'http://www.feriadosmunicipais.com.br/',
            'FDESANTANAMU1': 'https://www.diariooficial.feiradesantana.ba.gov.br/',
            'OABES': 'http://www.oab.org.br/leisnormas/boletiminfor',
            'EXRR1': 'http://www.imprensaoficial.rr.gov.br',
            'EXMTLIC': 'https://www.iomat.mt.gov.br/',
            'EXMT1': 'https://www.iomat.mt.gov.br/',
            'EXMSLIC': 'http://ww1.imprensaoficial.ms.gov.br/search/',
            'EXMS1': 'http://ww1.imprensaoficial.ms.gov.br/search/',
            'EXSP1LIC': 'http://www.imprensaoficial.com.br',
            'EXRNLIC': 'http://www.diariooficial.rn.gov.br/',
            'EXRJLIC' :'http://www.imprensaoficial.rj.gov.br/portal/modules/content/index.php?id=21',
            'EXPELIC': 'http://www.cepe.com.br/templates/cepe/images/btAcessoDiario.png',
            'EXMGLIC': 'http://www.iof.mg.gov.br/',
            'EXALLIC': 'http://www.imprensaoficialal.com.br/diario-oficial/',
            'EXSP1': 'http://www.imprensaoficial.com.br',
            'EXSP2': 'http://www.imprensaoficial.com.br',
            'EXSP3': 'http://localhost/alerte_bc/',
            'CONFERIR_EXSP3': 'https://www.fazenda.sp.gov.br/DiarioEletronico/ConsultaPublica.aspx',
            'EXSE1': 'https://segrase.se.gov.br/',
            'EXSC1': 'http://www.doe.sea.sc.gov.br/Portal/VisualizarCanal.aspx?cdCanal=42',
            'EXRS1': 'http://www.diariooficial.rs.gov.br/#/',
            'EXRO1': 'http://www.diof.ro.gov.br/',
            'EXRN1': 'http://www.diariooficial.rn.gov.br/',
            'EXRJP1': ' http://www.imprensaoficial.rj.gov.br/portal/modules/content/index.php?id=21',
            'EXPR1': 'https://www.documentos.dioe.pr.gov.br/dioe/consultaPublicaPDF.do?action=pgLocalizar&enviado=true&numero=&dataInicialEntrada=&dataFinalEntrada=&search=&diarioCodigo=3&submit=Localizar&localizador=',
            'EXPI1': 'http://www.diariooficial.pi.gov.br/index.php',
            'EXPB1': 'http://www.paraiba.pb.gov.br/index.php?option=com_docman&task=cat_view&gid=81',
            'EXMG1': 'http://www.jornalminasgerais.mg.gov.br/',
            'EXMA1': 'http://www.diariooficial.ma.gov.br/public/index.jsf',
            'EXGO1': 'http://diariooficial.abc.go.gov.br/',
            'EXDF1': 'http://www.buriti.df.gov.br/ftp/',
            'EXCE2': 'http://pesquisa.doe.seplag.ce.gov.br/doepesquisa/sead.do?page=ultimasEdicoes&cmd=11&action=Ultimas',
            'EXCE1': 'http://pesquisa.doe.seplag.ce.gov.br/doepesquisa/sead.do?page=ultimasEdicoes&cmd=11&action=Ultimas',
            'EXBA1A': 'http://www2.egba.ba.gov.br/diario/_DODia/DO_frm0.html',
            'EXBA1': 'http://diarios.egba.ba.gov.br/html/_DODia/DO_frm0.html',
            'EXAP1': 'http://sead.ap.gov.br/',
            'EXAM1': 'http://www.imprensaoficial.am.gov.br/',
            'EXAL1': 'http://www.imprensaoficialal.com.br/diario-oficial/',
            'EXAC1': 'http://www.diario.ac.gov.br/',
            'EXPE': 'http://www.cepe.com.br/',
            'EPSE': 'https://segrase.se.gov.br/',
            'EPPE': 'http://www.cepe.com.br/templates/cepe/images/btAcessoDiario.png',
            'EPPB1': 'http://www.paraiba.pb.gov.br/index.php?option=com_docman&task=cat_view&gid=81',
            'EPSP': 'https://www.imprensaoficial.com.br/',
            'EPTO': 'http://diariooficial.to.gov.br/',
            'EPRS': 'http://www.diariooficial.rs.gov.br/#/',
            'EPPR': 'https://www.documentos.dioe.pr.gov.br/dioe/consultaPublicaPDF.do?action=pgLocalizar&enviado=true&numero=&dataInicialEntrada=&dataFinalEntrada=&search=&diarioCodigo=2&submit=Localizar&localizador=', 
            'EPPE': 'http://www.cepe.com.br/',
            'EPMA': 'http://www.diariooficial.ma.gov.br/public/index.jsf',
            'EPMALIC': 'http://www.diariooficial.ma.gov.br/public/index.jsf',
            'EPMG': 'http://www.jornalminasgerais.mg.gov.br/',
            'EPBA': 'http://www2.egba.ba.gov.br/diario/_DODia/DO_frm0.html',
            'EPAL': 'http://www.imprensaoficialal.com.br/',
            'EPCE': 'http://pesquisa.doe.seplag.ce.gov.br/doepesquisa/sead.do?page=ultimasEdicoes&cmd=11&action=Ultimas',
            'EETO1': 'http://www.tjto.jus.br/',
            'EERS1': 'https://www.tjrs.jus.br/site/publicacoes/',
            'EEMGFI': 'https://dje.tjmg.jus.br/ultimaEdicao.do', 
            'EEMA1': 'http://www.tjma.jus.br/inicio/diario',
            'EEGO1': 'http://www.tjgo.jus.br/',
            'EEEPMA': 'http://www.diariooficial.ma.gov.br/public/index.jsf',
            'EERJTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'EESPTRT2': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'EEDF1': 'http://www.buriti.df.gov.br/ftp/',
            'EEDO3': 'http://portal.in.gov.br/',
            'EEDO2': 'http://portal.in.gov.br/',
            'EEDO1': 'http://portal.in.gov.br/',
            'EESPTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'EESPE2': 'http://www.imprensaoficial.com.br',
            'EESPE1': 'http://www.imprensaoficial.com.br',
            'EERJTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'EEPOAMU1': 'http://www2.portoalegre.rs.gov.br/portal_pmpa_novo/',
            'EEEXMA1': 'http://www.diariooficial.ma.gov.br/public/index.jsf',
            'EEEXGO1': 'http://diariooficial.abc.go.gov.br/',
            'EEBRTST': 'https://aplicacao2.jt.jus.br/dejt/f/n/diariocon',
            'EEBRSTF': 'http://www.stf.jus.br/portal/diariojusticaeletronico/pesquisardiarioeletronico.asp#',
            'EETRF4': 'http://www2.trf4.jus.br/trf4/',
            'ESTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'ESTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'ESMP': 'http://dimpes.mpes.mp.br/',
            'ESMU1': 'https://www.diariomunicipal.es.gov.br/',
            'ESMULIC': 'https://www.diariomunicipal.es.gov.br/',
            'ESJF': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx',
            'ESDO': 'https://dio.es.gov.br/portal/visualizacoes/diario_oficial',
            'ESDJ': 'http://www.tjes.jus.br/',
            'DTM1A': 'https://www.mar.mil.br/tm',
            'DTM1': 'https://www.marinha.mil.br/tm/',
            'MPDFT': 'http://www.mpdft.mp.br/portal/index.php/servicos-menu',
            'DFTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'DFTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'DFJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'DFDJ': 'http://www.tjdft.jus.br/',
            'DEC1': 'https://dec.prefeitura.sp.gov.br/portal/#/',
            'CNMP1': 'https://diarioeletronico.cnmp.mp.br/apex/f?p=102:1:0::NO:1:P1_DT_PUBLICACAO',
            'CTBAMU1A': 'http://www.curitiba.pr.gov.br/servicos/empresa/publicacao-dos-atos-oficiais-do-municipio-de-curitiba-diario-oficial/1032',
            'CTBAMU1': 'http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx',
            'CORRENTINAMU1': 'http://www.correntina.ba.io.org.br/diarioOficial',
            'CONTAGEMMU1': 'http://www.contagem.mg.gov.br/?se=doc',
            'CONGRESSO1': 'http://legis.senado.gov.br/diarios/PublicacoesOficiais',
            'CGRANDEMU1': 'http://www.pmcg.ms.gov.br/diogrande/',
            'CETRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'CETRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'CEJF': 'https://www.trf5.jus.br/',
            'CEDJ': 'http://esaj.tjce.jus.br/cdje/index.do;jsessionid=B0F79F57AF2EE1B70F5DB144DDA83AD1.cdje1',
            'CEDJA': 'http://www.tjce.jus.br/servicos/servicos_diario_justica.asp',
            'CEMP': 'http://consultaexternadoe.mpce.mp.br/',
            'CAXIASMU1': 'http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html',
            'CARIACICAMU1': 'http://www.cariacica.es.gov.br/publicacoes/diario-oficial/',
            'CAMRIO': 'http://www.camara.rj.gov.br/dcm_visualiza.php', 
            'CAMPOSMU1': 'http://www.campos.rj.gov.br/diario-oficial.php',
            'CAMPDO': 'http://www.campinas.sp.gov.br/',
            'CUIABAMU1': 'http://www.tce.mt.gov.br/diario',
            'BRAGPAULISTAMU1': 'https://www.imprensaoficialmunicipal.com.br/bragancapaulista',
            'SUPBR': 'http://portal.in.gov.br/',
            'DO3TRANSP': 'http://portal.in.gov.br/',
            'DO3LIC': 'http://portal.in.gov.br/',
            'DO3ENERGIA': 'http://portal.in.gov.br/',
            'DO3BR': 'http://portal.in.gov.br/',
            'DO3A': 'http://portal.in.gov.br/',
            'DO2X': 'http://portal.in.gov.br/',
            'DO2TRANSP': 'http://portal.in.gov.br/',
            'DO1X': 'http://portal.in.gov.br/',
            'DO1TRANSP': 'http://portal.in.gov.br/',
            'DO1F': 'http://portal.in.gov.br/',
            'DO1E': 'http://portal.in.gov.br/',
            'DO1D': 'http://portal.in.gov.br/',
            'DO1C': 'http://portal.in.gov.br/',
            'DO1BR': 'http://portal.in.gov.br/',
            'DO1B': 'http://portal.in.gov.br/',
            'DO1A': 'http://portal.in.gov.br/',
            'BRDO2': 'http://portal.in.gov.br/',
            'BRDO1': 'http://portal.in.gov.br/',
            'CNJBR': 'http://www.cnj.jus.br/',
            'BROXOMU1': 'http://prefeituradebelfordroxo.rj.gov.br/atos-oficiais/',
            'BRCSJT': 'http://www.csjt.jus.br/diario-eletronico-da-jt',
            'BRTSE': 'http://www.tse.jus.br/servicos-judiciais/publicacoes-oficiais/diario-da-justica-eletronico/diario-da-justica-eletronico-1',
            'BRTST': 'https://aplicacao2.jt.jus.br/dejt/f/n/diariocon', 
            'BRTRF5': 'https://www.trf5.jus.br/',
            'BRTRF1': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'BRSTM': 'https://www.stm.jus.br/servicos-stm/juridico/diario-de-justica-eletronico-dje', 
            'BRSTJ': 'http://www.stj.jus.br/portal/site/STJ',
            'BRSTF': 'http://www.stf.jus.br/portal/diariojusticaeletronico/pesquisardiarioeletronico.asp#',
            'BOAVISTAMU1': 'http://www.boavista.rr.gov.br/diario-oficial',
            'BHMU1': 'http://portal6.pbh.gov.br/dom/iniciaEdicao.do?method=DomDia',
            'BETIMMU1': 'http://www.betim.mg.gov.br/orgaooficial/',
            'BELMU1': 'http://www.belem.pa.gov.br/diarioom/index.jsf',
            'BELROXOMU1': 'http://noticiasdebelfordroxo.blogspot.com.br/p/atos-oficiais-da-prefeitura-de-broxo.html', 
            'BAMU1': 'http://diarios.egba.ba.gov.br/html/_DODia/DO_frm0.html',
            'BATRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'BATCM': 'http://www.tcm.ba.gov.br/',
            'BARUERIMU1': 'http://www.barueri.sp.gov.br/',
            'BATRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'BALIC': 'http://diarios.egba.ba.gov.br/html/_DODia/DO_frm0.html',
            'BALEG': 'http://egbanet.egba.ba.gov.br/alba',
            'BAJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'BADJSI': 'http://www5.tj.ba.gov.br/index.php',
            'BADJ': 'http://www5.tj.ba.gov.br/index.php',
            'APTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'APJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'APTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'APDJ': 'http://app.tjap.jus.br/tucujuris/publico/dje/',
            'ARACAJUMU1': 'http://sga.aracaju.se.gov.br:5011/legislacao/faces/diario_form_pesq.jsp',
            'ANGRAMU1': 'http://www.angra.rj.gov.br/',
            'AMMP': 'http://www.mpam.mp.br/',
            'AMTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'AMTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'AMJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'AMDJ': 'http://www.tjam.jus.br/',
            'ALTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'ALJF': 'https://www.trf5.jus.br/',
            'ALTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'ALCO': 'http://www2.tjal.jus.br/cdje/index.do',
            'ALDJ': 'http://www2.tjal.jus.br/cdje/index.do',
            'ACTRE1': 'http://www.tse.jus.br/servicos-judiciais/diario-da-justica-eletronico-1',
            'ACTRT': 'https://dejt.jt.jus.br/dejt/f/n/diariocon',
            'ACMP': 'http://www.mpac.mp.br/',
            'ACJF': 'http://portal.trf1.jus.br/portaltrf1/pagina-inicial.htm',
            'ALOAB1': 'http://www.imprensaoficialal.com.br/',
            'ACDJ': 'http://diario.tjac.jus.br/edicoes.php',
        
        } 

        self.texto_da_box_caderno = wx.StaticText(self.panel, wx.ID_ANY, "Digite o caderno:", (20, 15))
        
        self.box_caderno = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 35),size=(150, -1),style=wx.TE_PROCESS_ENTER)
        self.box_caderno.Bind(wx.EVT_TEXT_ENTER, self.abrir_site)

        self.button_abrir_site = wx.Button(self.panel, wx.ID_ANY, 'Abrir site', (200, 35)) 
        self.button_abrir_site.Bind(wx.EVT_BUTTON, self.abrir_site)

        self.frame.Show()
        self.frame.Centre()

    def abrir_site(self,event):
        try:
            site = self.dic_sites[self.box_caderno.GetLineText(0).upper()]
            webbrowser.open(site)
            self.statusbar.SetStatusText('Abrindo site do: {site}'.format(site=self.box_caderno.GetLineText(0).upper()))
            self.box_caderno.SetValue("")
            time.sleep(1)
            self.statusbar.SetStatusText('')
        except:
            dlg_box_box_caderno = wx.MessageDialog(None , u"Nunca nem vi esse caderno...",u"não achei o site...", wx.OK| wx.ICON_QUESTION) 
            dlg_box_box_caderno.ShowModal()

class UI_EDITOR_DE_PDF(Thread,object):
    """docstring for UI_EDITOR_DE_PDF"""
    def __init__(self, arg):
        super(UI_EDITOR_DE_PDF, self).__init__()
        self.frame = wx.Frame(None, -1, 'Editor de PDF', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,450,250)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.numero_de_paginas = None

        self.lista_paginas_para_cria_novo_pdf = []
        self.path_do_pdf = None
        
        ############################ TEXT BOX E STATIC BOX ###################################
        
        self.texto_da_box_pdf = wx.StaticText(self.panel, wx.ID_ANY, "PDF:", (20, 10))
        self.box_pdf = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 25),size=(270, -1),style=wx.TE_READONLY)

        self.texto_da_box_total_de_paginas = wx.StaticText(self.panel, wx.ID_ANY, "Total de páginas:", (20, 50))
        self.box_pdf_total_de_paginas = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 65),size=(50, -1),style=wx.TE_READONLY)   
        
        self.texto_da_box_nome_do_novo_pdf = wx.StaticText(self.panel, wx.ID_ANY, "Nome do novo PDF:", (20, 100))
        self.box_nome_do_novo_pdf = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 120),size=(150, -1))  
        
        self.texto_da_box_nova_formatacao_pdf = wx.StaticText(self.panel, wx.ID_ANY, "Nova formatação de PDF:", (20, 150))
        self.box_nova_formatacao_pdf = wx.TextCtrl(self.panel, wx.ID_ANY,"", (20, 170),size=(150, -1))  

        ################################### BOTOES ###########################################
        self.acoes = ['Separar', 'Excluir', 'Folha por folha'] 
          
        self.radio_box_acoes = wx.RadioBox(self.panel, wx.ID_ANY, label = 'Ação', pos = (200,100), choices = self.acoes, majorDimension = 1)
        self.radio_box_acoes.Bind(wx.EVT_RADIOBOX,self.escolha_de_acao)
        
        self.button_selecionar_pdf = wx.Button(self.panel, wx.ID_ANY, 'Selecionar PDF', (350, 20))
        self.button_selecionar_pdf.Bind(wx.EVT_BUTTON, self.buscar_pdf)
        
        self.button_criar_novo_pdf = wx.Button(self.panel, wx.ID_ANY, 'Criar novo PDF', (350, 50))
        self.button_criar_novo_pdf.Bind(wx.EVT_BUTTON, self.interpretar_intervalos)
        
        
        self.frame.Show()
        self.frame.Centre()
        
    def escolha_de_acao(self,event):
        return self.radio_box_acoes.GetStringSelection()
    
    def buscar_pdf(self,event):
        openFileDialog = wx.FileDialog(self.frame, "Selecione o PDF", "", "", 
                                      "Arquivos de PDF (*.pdf)|*.pdf", 
                                      wx.OPEN | wx.MULTIPLE)
        openFileDialog.ShowModal()
        try:
            if openFileDialog.GetPath() != '' or openFileDialog.GetPath() != None: 
                path_do_pdf = openFileDialog.GetPath()
                self.box_pdf.SetValue(path_do_pdf)
                self.path_do_pdf = path_do_pdf
                self.verificar_total_de_paginas(event= event, path= path_do_pdf)
                
                
        except:
            openFileDialog.Destroy()
        
        openFileDialog.Destroy()
    
    def verificar_total_de_paginas(self,event,path):
        pdf_reader =  PdfFileReader(path, "rb")
        self.numero_de_paginas = pdf_reader.getNumPages()
        self.box_pdf_total_de_paginas.SetValue('{}'.format(self.numero_de_paginas))
        
    def interpretar_intervalos(self,event):
        self.lista_paginas_para_cria_novo_pdf = []
        nova_formatacao = self.box_nova_formatacao_pdf.GetLineText(0).split(' ')
        for conjunto_de_paginas in nova_formatacao:
            intervalo_de_paginas = re.search(r'^([0-9]{1,}):([0-9]{1,})', conjunto_de_paginas)
            if intervalo_de_paginas:
               for pagina_intervalo in range(int(intervalo_de_paginas.group(1)),int(intervalo_de_paginas.group(2))+1):
                   self.lista_paginas_para_cria_novo_pdf.append(pagina_intervalo)
                   
            paginas_soltas = re.search(r'^([0-9]{1,})\,.*', conjunto_de_paginas)
            if paginas_soltas:
                lista_de_paginas = paginas_soltas.group()
                lista_de_paginas = lista_de_paginas.split(',')
                for pagina_solta in lista_de_paginas:
                    self.lista_paginas_para_cria_novo_pdf.append(int(pagina_solta))
            
            paginas_soltas_com_espaco = re.search(r'^[0-9]{1,}$', conjunto_de_paginas)
            if paginas_soltas_com_espaco:
                pag_solta_com_espaco = paginas_soltas_com_espaco.group()
                self.lista_paginas_para_cria_novo_pdf.append(int(pag_solta_com_espaco))
        
        if self.box_nome_do_novo_pdf.GetLineText(0) != '':
            self.criar_novo_pdf(event = event, pdf = self.path_do_pdf)
            print(u'Lista de páginas:') 
            print self.lista_paginas_para_cria_novo_pdf
            print(u'Total de páginas:')
            print len(self.lista_paginas_para_cria_novo_pdf)
            self.box_nova_formatacao_pdf.SetValue("")
            self.box_nome_do_novo_pdf.SetValue("")
            print("Pronto!!!")
        else:
            dlg_box_nome_do_novo_pdf = wx.MessageDialog(None , u"Seu filho esta sem nome, ponha um nome para seu novo PDF...","PDF sem nome..", wx.OK| wx.ICON_QUESTION) 
            dlg_box_nome_do_novo_pdf.ShowModal()

    def criar_novo_pdf(self,event,pdf):
        acao = self.escolha_de_acao(None)
        
        if acao == 'Separar' or acao == 'Excluir':
            pasta_temp = os.path.join(os.environ['USERPROFILE'], 'AppData','Local','Temp')
            print pasta_temp
            
            comando = 'A:\\Baixadores\\JCP\prgs\\sejda-console-3.2.71-bin\\sejda-console-3.2.71\\bin\sejda-console.bat merge -f {arquivo} -o {padrao_saida}'.format(arquivo=pdf, padrao_saida=os.path.join(pasta_temp, 'pdf_tratado.pdf'))
            if os.system(comando):
                erro = '############\n Erro no PDF \n############'
                print(erro)
            
            pasta_pdf_temp = os.path.join(os.environ['USERPROFILE'], 'AppData','Local','Temp','pdf_tratado.pdf')
            pdf_pdftk = PdfFileReader(pasta_pdf_temp, "rb")
            pdf_saida = PdfFileWriter()
            pasta_desktop =  os.path.join(os.environ['USERPROFILE'],'Desktop')
            
            if acao == 'Separar':
                for pagina in self.lista_paginas_para_cria_novo_pdf:
                            pagina_selecionada = pdf_pdftk.getPage(pagina-1)
                            pdf_saida.addPage(pagina_selecionada)
            
            if acao == 'Excluir':
                for pagina in range(1,self.numero_de_paginas+1):
                    if pagina not in self.lista_paginas_para_cria_novo_pdf: 
                        pagina_selecionada = pdf_pdftk.getPage(pagina-1)
                        pdf_saida.addPage(pagina_selecionada)
            
            with open(os.path.join(pasta_desktop,'{nome_do_pdf}.pdf'.format(nome_do_pdf=self.box_nome_do_novo_pdf.GetLineText(0))), 'wb') as f:
                pdf_saida.write(f)
            self.apagar_pdfs(event = event, path = pasta_pdf_temp)
        
        
        
        
        if acao == 'Folha por folha':
            pasta_folha_por_folha = os.path.join(os.environ['USERPROFILE'],'Desktop',self.box_nome_do_novo_pdf.GetLineText(0))
            os.makedirs(pasta_folha_por_folha) 
            paginas = []
            for pagina in self.lista_paginas_para_cria_novo_pdf:
                paginas.append(str(pagina))
            
            comando_folha_por_folha = 'A:\\Baixadores\\JCP\prgs\\sejda-console-3.2.71-bin\\sejda-console-3.2.71\\bin\sejda-console.bat splitbypages -f {arquivo} -o {padrao_saida} -n {paginas}'.format(arquivo=pdf, padrao_saida=pasta_folha_por_folha, paginas=' '.join(paginas))
            
            if os.system(comando_folha_por_folha):
                erro = '############\n Erro no PDF \n############'
                print(erro)


    def apagar_pdfs(self,event,path):
        try:
            shutil.rmtree(path)
        except:
            os.remove(path)

class UI_JCP(Thread,object):
    """docstring for UI_JCP"""
    def __init__(self, arg):
        super(UI_JCP, self).__init__()
        self.index = 0
        self.dia,self.mes,self.ano,self.caderno = None,None,None,None
        self.tipo_de_arq = None
        self.tipo_de_limpeza = None
        self.erro_pdftk = ''
        self.lista_sem_pdftk = []
        self.lista_de_pdfs = []
        self.data_do_p = None

        self.frame = wx.Frame(None, -1, 'Smart Box', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,610,600)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.statusbar.SetStatusText('O original não se desoriginaliza.')

        
        ################################### MENU ###########################################
        self.menu_cadernos_especiais = wx.Menu()
        self.aba_cadernos_int = self.menu_cadernos_especiais.Append(wx.ID_ANY, "Cadernos INT", "Cadernos INT")
        

        self.menu_ferramentas_de_conferencia = wx.Menu()
        self.aba_div = self.menu_ferramentas_de_conferencia.Append(wx.ID_ANY, "DIV", "DIV")
        self.aba_conferidor_da_baixacao = self.menu_ferramentas_de_conferencia.Append(wx.ID_ANY, "Conferidor baixação", "Conferidor baixação")
        self.aba_conferir_pdf_com_nnx = self.menu_ferramentas_de_conferencia.Append(wx.ID_ANY, "Conferir PDF com NNX", "Conferir PDF com NNX")
        self.aba_ler_pco_auto = self.menu_ferramentas_de_conferencia.Append(wx.ID_ANY, "Ler cadernos do PCO automático FDF", "Ler cadernos do PCO autamático FDF")
        self.aba_analisador_de_conjuntos = self.menu_ferramentas_de_conferencia.Append(wx.ID_ANY, "Analisador de conjuntos", "Analisador de conjuntos")

        self.menu_ferramentas = wx.Menu()
        self.aba_editor_de_pdf = self.menu_ferramentas.Append(wx.ID_ANY, "Editor de PDF", "Editor de PDF")
        self.aba_baixador = self.menu_ferramentas.Append(wx.ID_ANY, "Baixador", "Baixador")
        self.aba_buscar_pdf = self.menu_ferramentas.Append(wx.ID_ANY, "Buscar PDF", "Buscar PDF")
        self.aba_preparador_facil = self.menu_ferramentas.Append(wx.ID_ANY, "Comando PM", "Comando PM")
        self.aba_gerador_de_nnx_por_intervalos = self.menu_ferramentas.Append(wx.ID_ANY, "Gerador de nnx por intervalos", "Gerador de nnx por intervalos")
        self.aba_juntar_pdf_em_massa = self.menu_ferramentas.Append(wx.ID_ANY, "Juntar PDFs em massa", "Juntar PDFs em massa")
        
        self.menu_preparadores = wx.Menu()
        self.aba_preparador_trf1 = self.menu_preparadores.Append(wx.ID_ANY, "Preparador TRF1", "Preparador TRF1")
        self.aba_preparador_trt = self.menu_preparadores.Append(wx.ID_ANY, "Preparador TRT", "Preparador TRT")
        self.aba_preparador_municipais = self.menu_preparadores.Append(wx.ID_ANY, "Preparador Municipais", "Preparador Municipais")
        
        
        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_cadernos_especiais,"Cadernos especiais")
        self.menu_bar.Append(self.menu_ferramentas,"Ferramentas")
        self.menu_bar.Append(self.menu_ferramentas_de_conferencia,"Ferramentas de Conferência")
        self.menu_bar.Append(self.menu_preparadores,"Preparadores") 
        
        
        
        ################################# BINDS MENU ########################################
        self.frame.SetMenuBar(self.menu_bar)     
        self.frame.Bind(wx.EVT_MENU, self.buscar_cadernos_int, self.aba_cadernos_int)        
        self.frame.Bind(wx.EVT_MENU, self.juntar_pdf_em_massa, self.aba_juntar_pdf_em_massa) 
        self.frame.Bind(wx.EVT_MENU, self.abrir_editor_de_pdf, self.aba_editor_de_pdf)
        self.frame.Bind(wx.EVT_MENU, self.abrir_baixador, self.aba_baixador)
        self.frame.Bind(wx.EVT_MENU, self.abrir_buscar_pdf, self.aba_buscar_pdf)
        self.frame.Bind(wx.EVT_MENU, self.abrir_div, self.aba_div)
        self.frame.Bind(wx.EVT_MENU, self.abrir_conferidor_da_baixacao, self.aba_conferidor_da_baixacao)
        self.frame.Bind(wx.EVT_MENU, self.abrir_conferir_pdf_com_nnx, self.aba_conferir_pdf_com_nnx)
        self.frame.Bind(wx.EVT_MENU, self.abrir_ler_pco_auto, self.aba_ler_pco_auto)
        self.frame.Bind(wx.EVT_MENU, self.abrir_analisador_de_conjuntos, self.aba_analisador_de_conjuntos)
        self.frame.Bind(wx.EVT_MENU, self.abrir_preparador_trf1, self.aba_preparador_trf1)
        self.frame.Bind(wx.EVT_MENU, self.abrir_preparador_trt, self.aba_preparador_trt)
        self.frame.Bind(wx.EVT_MENU, self.abrir_preparador_municipais, self.aba_preparador_municipais)
        self.frame.Bind(wx.EVT_MENU, self.abrir_preparador_facil, self.aba_preparador_facil)
        self.frame.Bind(wx.EVT_MENU, self.abrir_gerador_de_nnx_por_intervalos, self.aba_gerador_de_nnx_por_intervalos)
        ################################### BOTOES ###########################################

        wx.StaticBox(self.panel, wx.ID_ANY, 'Opções', (360, 5), size=(200, 235))
        
        self.button_selecionar_pdf = wx.Button(self.panel, wx.ID_ANY, 'Selecionar PDF', (375, 25))
        self.button_selecionar_pdf.Bind(wx.EVT_BUTTON, self.buscar_pdf)
        
        self.button_pagar_pdf_da_lista = wx.Button(self.panel, wx.ID_ANY, 'Apagar', (375, 50))
        self.button_pagar_pdf_da_lista.Bind(wx.EVT_BUTTON, self.apagar_pdf_da_lista)

        self.button_pagar_pdfs_da_lista = wx.Button(self.panel, wx.ID_ANY, 'Limpar tudo', (375, 75))
        self.button_pagar_pdfs_da_lista.Bind(wx.EVT_BUTTON, self.apagar_de_pdfs_lista)

        self.button_preparar = wx.Button(self.panel, wx.ID_ANY, 'Preparar', (250, 450),size=(100, 50))
        self.button_preparar.Bind(wx.EVT_BUTTON, self.prepara)

        ################################### CADERNO ###########################################

        wx.StaticBox(self.panel, wx.ID_ANY, 'Preparação', (5, 305), size=(350, 210))

        self.texto_da_box_caderno = wx.StaticText(self.panel, wx.ID_ANY, "Caderno:", (25, 325))
        self.box_caderno = wx.TextCtrl(self.panel, wx.ID_ANY,"", (80, 325),size=(270, -1))
        
        
        ################################### -P ###########################################
        

        self.checkbox_do_p =  wx.CheckBox(self.panel, wx.ID_ANY, "Para o dia (-p):", (250, 360))
        self.checkbox_do_p.Bind(wx.EVT_CHECKBOX,self.validar_p_checkbox)

        self.calendario_p = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (250, 380),style=wx.DP_DROPDOWN)
        self.calendario_p.Enable(False)
        
        # self.box_p = wx.TextCtrl(self.panel, wx.ID_ANY,"", (250, 380),size=(100, -1))
        # self.box_p.Enable(False)
        

        
        ################################### CALENDARIO ###########################################
        self.calendario = wx.calendar.CalendarCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (25, 360))
        self.calendario.Bind(wx.calendar.EVT_CALENDAR,self.prepara)

        ################################### JUNTAR ###########################################
        self.texto_da_box_nome_do_novo_pdf = wx.StaticText(self.panel, wx.ID_ANY, u"Nome do novo PDF:", (375, 150))
        self.box_nome_do_novo_pdf = wx.TextCtrl(self.panel, wx.ID_ANY,"", (375, 175),size=(150, -1))
        
        self.button_de_juntar = wx.Button(self.panel, wx.ID_ANY, 'Juntar', (375, 205))
        self.button_de_juntar.Bind(wx.EVT_BUTTON, self.juntar_pdf_local)

         
        wx.StaticBox(self.panel, wx.ID_ANY, 'Diálogo', (365, 305), size=(230, 210))

        self.box_para_print = wx.TextCtrl(self.panel, wx.ID_ANY,"", (375, 325),size=(210, 175),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)
        
        ###################################LISTA CLRT###########################################
        id=wx.NewId()
        self.list = wx.ListCtrl(self.panel,id,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(350,300))      
        self.list.InsertColumn(0,"PDFs",width=1000)
        self.list.Show(True)
        
        
        self.frame.Show()
        self.frame.Centre()
    
    
    
    def juntar_pdf_em_massa (self,event):
        
        dlg_juntar_pdf_em_massa = wx.MessageDialog(None , "Todos os PDFs que deseja juntar estão na pasta:\n C:\\tmp ", "Juntar",wx.YES_NO | wx.ICON_QUESTION)
        result = dlg_juntar_pdf_em_massa.ShowModal()
        if result == wx.ID_YES:
            comando_juntar_pdf_em_massa = 'pdftk c:\\tmp\\*.pdf cat output {pasta}'.format(pasta=os.path.join(os.environ['USERPROFILE'],'Desktop','pdfs_do_tmp.pdf'))
            if os.system(comando_juntar_pdf_em_massa):
                erro = '############\n Erro ao juntar PDF\n############\n'
                raise Exception(erro)
            else:
                self.printar_na_box(event=event,texto='Seus PDFs da pasta C:\\tmp\nforam juntados com sucesso.')
    
    
    
    def abrir_preparador_municipais(self,event):
        os.startfile(os.path.join('A:\\Baixadores\\BAIXADOR_MUNIPAIS\\preparador_municipais.py'))
    
    def abrir_preparador_trt(self,event):
        os.startfile(os.path.join('A:\\Baixadores\BAIXADOR_TRT\\criar_trts.py'))
    
    
    def abrir_preparador_trf1(self,event):
        os.startfile(os.path.join('A:\\Baixadores\BAIXADOR_TRF1\\preparador_trf1.py'))
        
    
    def abrir_preparador_facil(self,event):
        p = UI_COMANDO_PM()
        p.start()
    
    def abrir_gerador_de_nnx_por_intervalos(self,event):
        p = UI_GERADOR_DE_NNX_POR_INTERVALOS()
        p.start()


    def abrir_analisador_de_conjuntos(self,event):
        p = UI_ANALISADOR_DE_CONJUNTOS(None)
        p.start()
    
    def abrir_ler_pco_auto(self,event):
        p = UI_LER_PCO_AUTO(None)
        p.start()

    def abrir_conferir_pdf_com_nnx (self,event):
        p = UI_conferir_pdf_com_nnx(None)
        p.start()
    
    def abrir_conferidor_da_baixacao (self,event):
        p = UI_conferidor_baixacao(None)
        p.start()
    
    def abrir_div (self,event):
        p = UI_DIV(None)
        p.start()

    def abrir_buscar_pdf (self,event):
       p = UI_abrir_pdf(None)
       p.start()

    def abrir_baixador (self,event):
        p = UI_BAIXADOR(None)
        p.start()
    
    def abrir_editor_de_pdf (self,event):
        p = UI_EDITOR_DE_PDF(None)
        p.start()

    def printar_na_box(self, event,texto):
        self.box_para_print.AppendText(texto)
        self.box_para_print.AppendText('\n')
    
    
    def buscar_cadernos_int(self,event):
        openFileDialog = wx.FileDialog(self.frame, "Selecione o CSV", "", "", 
                                      "Arquivos de CSV (*.csv)|*.csv", 
                                      wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
 
        openFileDialog.ShowModal()
        try:
            if openFileDialog.GetPaths() != '' or openFileDialog.GetPaths() != None: 
                for file in openFileDialog.GetPaths():
                    self.incluir_na_lista(file)
        except:
            openFileDialog.Destroy()
        
        openFileDialog.Destroy()
        self.tipo_de_arq = 'CSV'  
    
    def validar_p_checkbox(self,event):
        if self.checkbox_do_p.Value == False:
            self.calendario_p.Enable(False)
            # self.box_p.SetValue("")
        else:
            self.calendario_p.Enable(True)
    
    def juntar_pdf_local(self,event):
        nome_do_novo_pdf = self.box_nome_do_novo_pdf.GetLineText(0)
        if nome_do_novo_pdf != '':
            self.juntar_pdfs(event= event, pasta_de_rotina = os.path.join(os.environ['USERPROFILE'],'Desktop'),nome_do_pdf='{nome_do_pdf}.pdf'.format(nome_do_pdf=nome_do_novo_pdf)) 
            self.box_nome_do_novo_pdf.SetValue("")      
        else:
            dlg_box_nome_do_novo_pdf = wx.MessageDialog(None , u"Seu filho esta sem nome, ponha um nome para seu novo PDF...","PDF sem nome..", wx.OK| wx.ICON_QUESTION) 
            dlg_box_nome_do_novo_pdf.ShowModal()

    
    def juntar_pdfs(self,event,pasta_de_rotina,nome_do_pdf):
        self.criar_lista_de_pdfs(None)
        if len(self.lista_de_pdfs) >= 2:
            self.printar_na_box(event=event,texto='{pasta}'.format(pasta=pasta_de_rotina))
            self.lista_sem_pdftk = self.lista_de_pdfs 
            pdfs = ' '.join(self.lista_de_pdfs)
            
            try:
                self.printar_na_box(event=event,texto='Juntando arquivos...')
                pasta_do_pdf = os.path.join(pasta_de_rotina, "{nome_do_pdf}".format(nome_do_pdf=nome_do_pdf))
                comando = 'A:\\Baixadores\\JCP\prgs\\sejda-console-3.2.71-bin\\sejda-console-3.2.71\\bin\\sejda-console.bat merge -f {arquivo} -o {padrao_saida}'.format(arquivo=pdfs, padrao_saida=pasta_do_pdf)
                if os.system(comando):
                    erro = '############\n Erro ao juntar PDF\n############\n'
                    self.erro_pdftk = erro
                    raise Exception(erro)
                
                self.apagar_de_pdfs_lista(None) 
                self.printar_na_box(event=event,texto="Pronto!")
                self.tipo_de_limpeza = 'LISTA'
            except:
                self.printar_na_box(event=event,texto='\nOPS... erro ao juntar...')
                time.sleep(2)
        else:
            pasta_de_rotina
            self.printar_na_box(event=event,texto='{pasta}'.format(pasta=pasta_de_rotina))
            self.printar_na_box(event=event,texto='Juntando arquivos...')
            for pdf in self.lista_de_pdfs:
                os.rename(pdf, '{pasta_de_rotina}\\{nome_do_pdf}'.format(pasta_de_rotina=pasta_de_rotina,nome_do_pdf=nome_do_pdf))
                self.apagar_de_pdfs_lista(None)
                self.tipo_de_limpeza = 'NADA'
                self.printar_na_box(event=event,texto="Pronto!")       

    def criar_dia_mes_ano(self,event,data):
        data  = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')
    
    
    def chamar_pm(self,event,status):
        self.printar_na_box(event=event,texto='Chamando PM')
        if status == True and self.checkbox_do_p.Value == True:
            # print('-p')
            todos_os_comandos = ['A', 'pm {caderno} -d {dia} -m {mes} -a {ano} -p {para_o_dia}'.format(caderno = self.caderno, dia = self.dia, mes = self.mes, ano = self.ano, para_o_dia = self.data_do_p)]
            cmd_str = '\n'.join(todos_os_comandos)+'\n'
            p = subprocess.Popen('cmd.exe', shell=True, cwd=r'a:\lido\cmd', stdin=subprocess.PIPE)
            p.stdin.write(cmd_str)
        
        if status == True and self.checkbox_do_p.Value == False:
            # print('normal')
            todos_os_comandos = ['A', 'pm {caderno} -d {dia} -m {mes} -a {ano}'.format(caderno = self.caderno, dia = self.dia, mes = self.mes, ano = self.ano)]
            cmd_str = '\n'.join(todos_os_comandos)+'\n'
            p = subprocess.Popen('cmd.exe', shell=True, cwd=r'a:\lido\cmd', stdin=subprocess.PIPE)
            p.stdin.write(cmd_str)
    
    def validar_p(self,event):
        if self.caderno not in CADENOS_DO_P:
            # self.calendario_p.Enable(True)
            return True
        if self.caderno in CADENOS_DO_P and self.checkbox_do_p.Value == True:
            # self.calendario_p.Enable(True)
            return True
        else:
            self.calendario_p.Enable(False)
            return False

    def criar_lista_de_pdfs(self,event):
        self.lista_de_pdfs = []
        numero_de_itens_na_lista = self.list.GetItemCount()
        if numero_de_itens_na_lista != 0:        
            for linha in range(numero_de_itens_na_lista):
                item = self.list.GetItem(itemId=linha, col=0)
                self.lista_de_pdfs.append(item.GetText())
        else:
            dlg_pdf = wx.MessageDialog(None , "Selecione pelo menos um PDF","Erro", wx.OK| wx.ICON_WARNING)
            dlg_pdf.ShowModal()
            self.buscar_pdf(None)
    
    def verificar_lista_vazia(self,event):
        
        if self.list.GetItemCount() == 0:
            dlg_pdf = wx.MessageDialog(None , "Selecione pelo menos um PDF","Erro", wx.OK| wx.ICON_WARNING)
            dlg_pdf.ShowModal()
            self.buscar_pdf(None)
            return False
        else:
            return True   
    
    def apagar_pdfs(self,event,path,tipo):
        time.sleep(3)
        if tipo == 'LISTA':
            for pdf in path:        
                try:
                    shutil.rmtree(pdf)
                except:
                    os.remove(pdf)
        if tipo == 'UNICO':
            try:
                shutil.rmtree(path)
            except:
                os.remove(path)
        if tipo == 'NADA':
            pass
        
            # finally:
            #     dlg_nao_apagou = wx.MessageDialog(None , "Tentei apagar mais o PDF esta ainda aberto...","Erro", wx.OK| wx.ICON_WARNING)
            #     dlg_nao_apagou.ShowModal()
    
    def prepara(self,event):
        self.caderno = self.box_caderno.GetLineText(0).upper()
        self.printar_na_box(event=event,texto='\n{caderno}'.format(caderno=self.caderno)) 
        if self.checkbox_do_p.Value == True:
            data_p = self.calendario_p.GetValue()
            dia_p,mes_p,ano_p = self.criar_dia_mes_ano(event=event,data=data_p)
            self.data_do_p = '{dia_p}/{mes_p}/{ano_p}'.format(dia_p=dia_p,mes_p=mes_p,ano_p=ano_p)
            
            self.printar_na_box(event=event,texto='O cadernor recebeu -p: {p}'.format(p=self.data_do_p))
        
        if self.caderno != '':
            status = self.validar_p(None)
            if status == True:
                data = self.calendario.GetDate()
                self.data = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
                self.dia,self.mes,self.ano = self.data.strftime('%d'),self.data.strftime('%m'),self.data.strftime('%Y')
                        
                pasta_de_rotina = os.path.join('L:\\', 'rotina', self.ano, self.mes, self.dia, 'download', self.caderno)
                resposta_para_criar = self.verificar_lista_vazia(None)
                if resposta_para_criar == True:
                    os.makedirs(pasta_de_rotina)
                    self.printar_na_box(event=event,texto='Criando pasta...')
                    if self.tipo_de_arq == 'CSV':
                        nome_do_arq = 'X.csv'
                    if self.tipo_de_arq == 'PDF':
                        nome_do_arq = 'X.pdf'                
                    self.juntar_pdfs(event= event, pasta_de_rotina = pasta_de_rotina ,nome_do_pdf=nome_do_arq)
                    os.startfile(os.path.join(pasta_de_rotina, nome_do_arq))
                    dlg_pm = wx.MessageDialog(None , "Tudo certo para fazer o PM?","Prepara", wx.YES_NO | wx.ICON_QUESTION)
                    result = dlg_pm.ShowModal()
                    if result == wx.ID_YES:
                        self.chamar_pm(event=event,status=status)
                        self.criar_relatorio_txt(event = event, caderno = self.caderno, dia = self.dia ,mes = self.mes, ano = self.ano, status_p = self.data_do_p)
                        self.box_caderno.SetValue("")
                        self.apagar_de_pdfs_lista(None)
                        self.calendario_p.Enable(False)
                        self.checkbox_do_p.SetValue(False) 
                        self.apagar_pdfs(event = event, path = self.lista_de_pdfs, tipo=self.tipo_de_limpeza)
                        self.apagar_pdfs(event = event, path = self.lista_sem_pdftk, tipo=self.tipo_de_limpeza)
                            
                            
                    else:
                        self.printar_na_box(event=event,texto='Apagando...')
                        self.printar_na_box(event=event,texto='{pasta}'.format(pasta=pasta_de_rotina)) 
                        self.apagar_pdfs(event = event, path = pasta_de_rotina, tipo='UNICO')
                        self.calendario_p.Enable(False)
                        self.checkbox_do_p.SetValue(False)
            else:
                dlg_box_p = wx.MessageDialog(None , u"Esse caderno tem o -p ou não estou conseguindo preparar.","Ops..", wx.OK| wx.ICON_WARNING)
                dlg_box_p.ShowModal()
        else:
            dlg_box_p = wx.MessageDialog(None , u"Nunca nem vi esse caderno...","Eita..", wx.OK| wx.ICON_QUESTION) 
            dlg_box_p.ShowModal()

    def buscar_pdf(self,event):
        openFileDialog = wx.FileDialog(self.frame, "Selecione o PDF", "", "", 
                                      "Arquivos de PDF (*.pdf)|*.pdf", 
                                      wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
 
        openFileDialog.ShowModal()
        try:
            if openFileDialog.GetPaths() != '' or openFileDialog.GetPaths() != None: 
                for file in openFileDialog.GetPaths():
                    self.incluir_na_lista(file)
        except:
            openFileDialog.Destroy()
        
        openFileDialog.Destroy()
        self.tipo_de_arq = 'PDF'

    def apagar_pdf_da_lista(self,event):
        item = self.list.GetFocusedItem()
        self.list.DeleteItem(item) 
    
    def apagar_de_pdfs_lista(self,event):
        self.list.DeleteAllItems()   

    def incluir_na_lista(self,event):
        self.list.InsertStringItem(self.index,event)
        self.index += 1

    def criar_relatorio_txt(self,event,caderno,dia,mes,ano,status_p):
        data_de_relatorio = datetime.datetime.now()
        r_dia,r_mes,r_ano = data_de_relatorio.strftime('%d'),data_de_relatorio.strftime('%m'),data_de_relatorio.strftime('%Y')
        with open((os.path.join('A:\\','Baixadores','JCP','Relatorio_JCP','{dia}-{mes}-{ano}-relatorio.txt'.format(dia=r_dia,mes=r_mes,ano=r_ano))), 'a+t') as arq_txt:
                
                linha_do_caderno = '\nCaderno: {Caderno}\n'.format(Caderno=caderno)
                arq_txt.write(linha_do_caderno)
                
                data_pasta_de_rotina = 'Dados da pasta Rotina: {dia}/{mes}/{ano}\n'.format(dia=self.dia,mes=self.mes,ano=self.ano)
                arq_txt.write(data_pasta_de_rotina)

                dados_de_preparacao = 'Dados de preparação: {}\n'.format(data_de_relatorio.strftime('%c'))
                arq_txt.write(dados_de_preparacao)

                linha_do_p = 'Para o dia (-p): {status}\n'.format(status=status_p)
                arq_txt.write(linha_do_p)
                
                arq_txt.write(self.erro_pdftk)

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()