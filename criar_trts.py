#!/usr/bin/env python
# -*- coding: latin-1

import wx
import wx.calendar
import os
import datetime
import re
import subprocess
import shutil
import fnmatch
import time


from PyPDF2 import PdfFileReader, PdfFileMerger

def main():
    UI_PREPARADOR_TRT()

class UI_BAIXADOR(object):
    """docstring for UI_BAIXADOR"""
    def __init__(self):
        super(UI_BAIXADOR, self).__init__()
        self.frame = wx.Frame(None, -1, 'Baixador', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,300,100)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        
        self.statusbar = self.frame.CreateStatusBar(1)

        self.texto_calendario = wx.StaticText(self.panel, wx.ID_ANY, "Data", (5, 5))
        self.calendario = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (5, 20),style=wx.DP_DROPDOWN)


        self.button_preparar = wx.Button(self.panel, wx.ID_ANY, 'Baixar', (150, 5), size=(100, 40))
        self.button_preparar.Bind(wx.EVT_BUTTON,self.baixar)

        self.frame.Show()
        self.frame.Centre()

    def criar_dia_mes_ano(self,data):
        data  = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')

    def baixar(self,event):
       data = self.calendario.GetValue()
       dia,mes,ano = self.criar_dia_mes_ano(data=data)
       comando = 'A:\\Baixadores\BAIXADOR_TRT\\baixador_trabalhista_datas.py -d {dia} -m {mes} -a {ano}'.format(dia=dia,mes=mes,ano=ano)
       if os.system(comando):
           erro = '############\n Erro \n############\n'




class UI_PREPARADOR_TRT(object):
    """docstring for UI_PREPARADOR_TRT"""
    def __init__(self):
        super(UI_PREPARADOR_TRT, self).__init__()
    
        self.frame = wx.Frame(None, -1, 'Preparador TRT', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,550,600)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.index = 0
        # self.listar_pdfs_path_download = None
        
        self.statusbar =  self.frame.CreateStatusBar(1)
        
        self.menu_baixador = wx.Menu()
        self.aba_baixador = self.menu_baixador.Append(wx.ID_ANY, "Baixador TRT", "Baixador TRT")

        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_baixador,"Baixador TRT")

        self.frame.SetMenuBar(self.menu_bar)     
        self.frame.Bind(wx.EVT_MENU, self.abrir_baixador_trt, self.aba_baixador)
        
        
        wx.StaticBox(self.panel, wx.ID_ANY, 'Pasta de rotina', (240, 5), size=(125, 75))
        wx.StaticBox(self.panel, wx.ID_ANY, 'Comando -p', (380, 5), size=(125, 75))
        wx.StaticBox(self.panel, wx.ID_ANY, 'Diálogo', (240, 180), size=(270, 215))
        
        self.dic_cadernos = [
            'CSJT > Conselho Superio (BRCSJT)',
            'TST > Tribunal Superior (BRTST)',
            'TRT1 > TRT 1 Regiao     (RJTRT)',
            'TRT2 > TRT 2 Regiao     (SPTRT2)',
            'TRT3 > TRT 3 Regiao     (MGTRT)',
            'TRT4 > TRT 4 Regiao     (RSTRT)',
            'TRT5 > TRT 5 Regiao     (BATRT)',
            'TRT6 > TRT 6 Regiao     (PETRT)',
            'TRT7 > TRT 7 Regiao     (CETRT)',
            'TRT8 > TRT 8 Regiao     (PATRT)',
            'TRT9 > TRT 9 Regiao     (PRTRT)',
            'TRT10 > TRT 10 Regiao   (DFTRT)',
            'TRT11 > TRT 11 Regiao   (AMTRT)',
            'TRT12 > TRT 12 Regiao   (SCTRT2)',
            'TRT13 > TRT 13 Regiao   (PBTRT)',
            'TRT14 > TRT 14 Regiao   (ROTRT)',
            'TRT15 > TRT 15 Regiao   (SPTRT)',
            'TRT16 > TRT 16 Regiao   (MATRT)',
            'TRT17 > TRT 17 Regiao   (ESTRT)',
            'TRT18 > TRT 18 Regiao   (GOTRT)',
            'TRT19 > TRT 19 Regiao   (ALTRT)',
            'TRT20 > TRT 20 Regiao   (SETRT)',
            'TRT21 > TRT 21 Regiao   (RNTRT)',
            'TRT22 > TRT 22 Regiao   (PITRT)',
            'TRT23 > TRT 23 Regiao   (MTTRT)',
            'TRT24 > TRT 24 Regiao   (MSTRT)',
            ] 
          
        self.radio_box_cadernos = wx.RadioBox(self.panel, wx.ID_ANY, label = 'Cadernos', pos = (10,10), choices = self.dic_cadernos, majorDimension = 1)
        
        
        
        
        self.button_preparar = wx.Button(self.panel, wx.ID_ANY, 'Preparar', (250, 100),size=(100, 50))
        self.button_preparar.Bind(wx.EVT_BUTTON,self.prepara)

        self.button_preparar = wx.Button(self.panel, wx.ID_ANY, 'Conferir', (400, 100),size=(100, 50))
        self.button_preparar.Bind(wx.EVT_BUTTON,self.conferir_caderno)


        self.texto_calendario_rotina = wx.StaticText(self.panel, wx.ID_ANY, "Rotina", (250, 25))
        self.calendario_rotina = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (250, 50),style=wx.DP_DROPDOWN)

        self.texto_calendario_p = wx.StaticText(self.panel, wx.ID_ANY, "-p", (390, 25))
        self.calendario_p = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (390, 50),style=wx.DP_DROPDOWN)
        
        self.box_para_print = wx.TextCtrl(self.panel, wx.ID_ANY,"", (250, 200),size=(250, 175),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)


        self.frame.Show()
        self.frame.Centre()


   
   
   
   
    def abrir_baixador_trt(self,event):
        UI_BAIXADOR()
        
       
    

    def buscar_ediao_do_trt(self):
        pasta_de_trt = os.path.join('A:\\','Baixadores','BAIXADOR_TRT','TRAB_BX')
        pasta_de_edicao = os.listdir(pasta_de_trt)
        pasta_de_edicao = pasta_de_edicao[0]
        return os.path.join(pasta_de_trt,pasta_de_edicao)
    
    
    def procurar(self,nome_do_arq,pasta_de_trts):

        for root, dirnames, filenames in os.walk(pasta_de_trts):
                for dirname in fnmatch.filter(dirnames, nome_do_arq):
                    arq = os.listdir(os.path.join(root, dirname))
                    try:
                        os.rename(os.path.join(root,dirname,arq[0]), os.path.join(root,dirname,'X.pdf'))
                    except:
                        pass
                    return os.path.join(root,dirname,'X.pdf')   
    
    
    def juntar_arquivos_pdf(self,lista_de_pdfs,pasta_de_rotina):

        merger = PdfFileMerger()
        self.printar_na_box(texto='Juntando arquivos...')
        for pdf in lista_de_pdfs:
            try:
                merger.append(PdfFileReader(pdf, "rb"))
            except:
                continue
        try:
            self.printar_na_box(texto='Criando pasta...')
            os.makedirs(pasta_de_rotina)    
            merger.write(os.path.join(pasta_de_rotina, "X.pdf"))
            os.startfile(os.path.join(pasta_de_rotina, "X.pdf"))
            self.printar_na_box(texto='Pronto!\n')
        except:
            self.printar_na_box(texto='\nOPS... acho que temos uma pasta para esse caderno.....\n')
            time.sleep(2)
        
    
    
    def formar_pasta_de_rotina(self,dia,mes,ano,caderno):
        return os.path.join('L:\\', 'rotina',ano, mes, dia, 'download',caderno)
    
    
    def printar_na_box(self,texto):
        self.box_para_print.AppendText(texto)
        self.box_para_print.AppendText('\n')
    
    def criar_dia_mes_ano(self,event,data):
        data  = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')
    
    
    def prepara_caderno(self,caderno,dia,mes,ano,data_do_comando_p):

        todos_os_comandos = ['A', 'pm {caderno} -d {dia} -m {mes} -a {ano} -p {data_do_comando_p}'.format(caderno=caderno,dia=dia,mes=mes,ano=ano,data_do_comando_p=data_do_comando_p)]

        cmd_str = '\n'.join(todos_os_comandos)+'\n'
        p = subprocess.Popen('cmd.exe', shell=True, cwd=r'a:\lido\cmd', stdin=subprocess.PIPE)
        p.stdin.write(cmd_str)
    
    
    def filtar_entrada(self):
        caderno_selecionado = self.radio_box_cadernos.GetStringSelection()

        self.dic_cadernos ={
            'CSJT > Conselho Superio (BRCSJT)': 'BRCSJT',
            'TST > Tribunal Superior (BRTST)': 'BRTST',
            'TRT1 > TRT 1 Regiao     (RJTRT)': 'RJTRT',
            'TRT2 > TRT 2 Regiao     (SPTRT2)': 'SPTRT2',
            'TRT3 > TRT 3 Regiao     (MGTRT)': 'MGTRT',
            'TRT4 > TRT 4 Regiao     (RSTRT)': 'RSTRT',
            'TRT5 > TRT 5 Regiao     (BATRT)': 'BATRT',
            'TRT6 > TRT 6 Regiao     (PETRT)': 'PETRT',
            'TRT7 > TRT 7 Regiao     (CETRT)': 'CETRT',
            'TRT8 > TRT 8 Regiao     (PATRT)': 'PATRT',
            'TRT9 > TRT 9 Regiao     (PRTRT)': 'PRTRT',
            'TRT10 > TRT 10 Regiao   (DFTRT)': 'DFTRT',
            'TRT11 > TRT 11 Regiao   (AMTRT)': 'AMTRT',
            'TRT12 > TRT 12 Regiao   (SCTRT2)': 'SCTRT2',
            'TRT13 > TRT 13 Regiao   (PBTRT)': 'PBTRT',
            'TRT14 > TRT 14 Regiao   (ROTRT)': 'ROTRT',
            'TRT15 > TRT 15 Regiao   (SPTRT)': 'SPTRT',
            'TRT16 > TRT 16 Regiao   (MATRT)': 'MATRT',
            'TRT17 > TRT 17 Regiao   (ESTRT)': 'ESTRT',
            'TRT18 > TRT 18 Regiao   (GOTRT)': 'GOTRT',
            'TRT19 > TRT 19 Regiao   (ALTRT)': 'ALTRT',
            'TRT20 > TRT 20 Regiao   (SETRT)': 'SETRT',
            'TRT21 > TRT 21 Regiao   (RNTRT)': 'RNTRT',
            'TRT22 > TRT 22 Regiao   (PITRT)': 'PITRT',
            'TRT23 > TRT 23 Regiao   (MTTRT)': 'MTTRT',
            'TRT24 > TRT 24 Regiao   (MSTRT)': 'MSTRT',
            }
        
        self.dic_tribunais ={
            'BRCSJT':['*Conselho Superior da Justi?a do Trabalho - Administrativo'],
            'BRTST': ['*Tribunal Superior do Trabalho - Judici?rio','*Tribunal Superior do Trabalho - Administrativo'],
            'RJTRT': ['*TRT da 1? Regi?o - Judici?rio','*TRT da 1? Regi?o - Administrativo'],
            'SPTRT2': ['*TRT da 2? Regi?o - Judici?rio','*TRT da 2? Regi?o - Administrativo'],
            'MGTRT': ['*TRT da 3? Regi?o - Judici?rio','*TRT da 3? Regi?o - Administrativo'],
            'RSTRT': ['*TRT da 4? Regi?o - Judici?rio','*TRT da 4? Regi?o - Administrativo'],
            'BATRT': ['*TRT da 5? Regi?o - Judici?rio','*TRT da 5? Regi?o - Administrativo'],
            'PETRT': ['*TRT da 6? Regi?o - Judici?rio','*TRT da 6? Regi?o - Administrativo'],
            'CETRT': ['*TRT da 7? Regi?o - Judici?rio','*TRT da 7? Regi?o - Administrativo'],
            'PATRT': ['*TRT da 8? Regi?o - Judici?rio','*TRT da 8? Regi?o - Administrativo'],
            'PRTRT': ['*TRT da 9? Regi?o - Judici?rio','*TRT da 9? Regi?o - Administrativo'],
            'DFTRT': ['*TRT da 10? Regi?o - Judici?rio','*TRT da 10? Regi?o - Administrativo'],
            'AMTRT': ['*TRT da 11? Regi?o - Judici?rio','*TRT da 11? Regi?o - Administrativo'],
            'SCTRT2': ['*TRT da 12? Regi?o - Judici?rio','*TRT da 12? Regi?o - Administrativo'],
            'PBTRT': ['*TRT da 13? Regi?o - Judici?rio','*TRT da 13? Regi?o - Administrativo'],
            'ROTRT': ['*TRT da 14? Regi?o - Judici?rio','*TRT da 14? Regi?o - Administrativo'],
            'SPTRT': ['*TRT da 15? Regi?o - Judici?rio','*TRT da 15? Regi?o - Administrativo'],
            'MATRT': ['*TRT da 16? Regi?o - Judici?rio','*TRT da 16? Regi?o - Administrativo'],
            'ESTRT': ['*TRT da 17? Regi?o - Judici?rio','*TRT da 17? Regi?o - Administrativo'],
            'GOTRT': ['*TRT da 18? Regi?o - Judici?rio','*TRT da 18? Regi?o - Administrativo'],
            'ALTRT': ['*TRT da 19? Regi?o - Judici?rio','*TRT da 19? Regi?o - Administrativo'],
            'SETRT': ['*TRT da 20? Regi?o - Judici?rio','*TRT da 20? Regi?o - Administrativo'],
            'RNTRT': ['*TRT da 21? Regi?o - Judici?rio','*TRT da 21? Regi?o - Administrativo'],
            'PITRT': ['*TRT da 22? Regi?o - Judici?rio','*TRT da 22? Regi?o - Administrativo'],
            'MTTRT': ['*TRT da 23? Regi?o - Judici?rio','*TRT da 23? Regi?o - Administrativo'],
            'MSTRT': ['*TRT da 24? Regi?o - Judici?rio','*TRT da 24? Regi?o - Administrativo'],
            }
    
        caderno = self.dic_cadernos[caderno_selecionado]
        pdfs_do_caderno = self.dic_tribunais[caderno]

        return caderno,pdfs_do_caderno

    def conferir_caderno(self,event):
        
        caderno,pdfs_do_caderno = self.filtar_entrada()
        self.printar_na_box(texto='Caderno: {caderno}'.format(caderno=caderno))

        pasta_de_edicao_trt = self.buscar_ediao_do_trt()

        pasta_de_local = os.path.join(os.environ['USERPROFILE'], 'Desktop',caderno)

        lista_de_pdfs = []
        for pdf in pdfs_do_caderno:
            pasta_de_pdf = self.procurar(nome_do_arq=pdf,pasta_de_trts=pasta_de_edicao_trt)
            lista_de_pdfs.append(pasta_de_pdf)

        self.juntar_arquivos_pdf(lista_de_pdfs=lista_de_pdfs,pasta_de_rotina=pasta_de_local)
    
    
    def prepara(self,event):
        
        caderno,pdfs_do_caderno = self.filtar_entrada()
        
        data = self.calendario_rotina.GetValue()
        dia,mes,ano = self.criar_dia_mes_ano(event=event,data=data)
        
        data_p = self.calendario_p.GetValue()
        dia_p,mes_p,ano_p = self.criar_dia_mes_ano(event=event,data=data_p)
        data_do_comando_p = '{dia_p}/{mes_p}/{ano_p}'.format(dia_p=dia_p,mes_p=mes_p,ano_p=ano_p)
        pasta_de_rotina = self.formar_pasta_de_rotina(dia=dia,mes=mes,ano=ano,caderno=caderno)
        
        self.printar_na_box(texto='Caderno: {caderno}'.format(caderno=caderno))
        self.printar_na_box(texto='{pasta}'.format(pasta=pasta_de_rotina))
        
        pasta_de_edicao_trt = self.buscar_ediao_do_trt()
        
        lista_de_pdfs = []
        for pdf in pdfs_do_caderno:
            pasta_de_pdf = self.procurar(nome_do_arq=pdf,pasta_de_trts=pasta_de_edicao_trt)
            lista_de_pdfs.append(pasta_de_pdf)
        
        
        self.juntar_arquivos_pdf(lista_de_pdfs=lista_de_pdfs,pasta_de_rotina=pasta_de_rotina)
        
        dlg_pm = wx.MessageDialog(None , "Tudo certo para fazer o PM?","Prepara", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg_pm.ShowModal()
        
        if result == wx.ID_YES:
            self.prepara_caderno(caderno=caderno,dia=dia,mes=mes,ano=ano,data_do_comando_p=data_do_comando_p)


if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()