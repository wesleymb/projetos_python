#!/usr/bin/env python
# -*- coding: latin-1

import wx
import wx.calendar
import os
import datetime
import re
import subprocess
import shutil

# path_download = os.path.join('C:\\','Users','lido-dev','Desktop','BAIXADOR_TRF1','TRF1_BX')

path_download = os.path.join('A:\\','Baixadores','BAIXADOR_TRF1','TRF1_BX') 

def main():
    UI_PREPARADOR_TRF1()

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
       comando = 'A:\\Baixadores\BAIXADOR_TRF1\\baixador_trf1_datas.py -d {dia} -m {mes} -a {ano}'.format(dia=dia,mes=mes,ano=ano)
       if os.system(comando):
           erro = '############\n Erro \n############\n'





class UI_PREPARADOR_TRF1(object):
    """docstring for UI_PREPARADOR_TRF1"""
    def __init__(self):
        super(UI_PREPARADOR_TRF1, self).__init__()

              
        self.frame = wx.Frame(None, -1, 'Preparador TRF1', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,625,475)
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.index = 0
        # self.listar_pdfs_path_download = None

        self.statusbar =  self.frame.CreateStatusBar(1)
        
        self.menu_baixador = wx.Menu()
        self.aba_baixador = self.menu_baixador.Append(wx.ID_ANY, "Baixador TRF1", "Baixador TRF1")
        self.aba_preparador_trf1est = self.menu_baixador.Append(wx.ID_ANY, "Preparador TRF1EST", "Preparador TRF1EST")

        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_baixador,"Baixador TRF1")

        self.frame.SetMenuBar(self.menu_bar)     
        self.frame.Bind(wx.EVT_MENU, self.abrir_baixador_trf1, self.aba_baixador)
        self.frame.Bind(wx.EVT_MENU, self.prepara_trf1est,  self.aba_preparador_trf1est)
        
        
        wx.StaticBox(self.panel, wx.ID_ANY, 'PDFs baixados', (10, 5), size=(325, 410))
        wx.StaticBox(self.panel, wx.ID_ANY, 'Pasta de rotina', (340, 5), size=(125, 75))
        wx.StaticBox(self.panel, wx.ID_ANY, 'Comando -p', (480, 5), size=(125, 75))
        wx.StaticBox(self.panel, wx.ID_ANY, 'Diálogo', (340, 180), size=(270, 215))
        
        self.texto_calendario_rotina = wx.StaticText(self.panel, wx.ID_ANY, "Rotina", (350, 25))
        self.calendario_rotina = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (350, 50),style=wx.DP_DROPDOWN)

        self.texto_calendario_p = wx.StaticText(self.panel, wx.ID_ANY, "-p", (500, 25))
        self.calendario_p = wx.DatePickerCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), (500, 50),style=wx.DP_DROPDOWN)

        self.button_atulizar = wx.Button(self.panel, wx.ID_ANY, 'Atualizar', (20, 25))
        self.button_atulizar.Bind(wx.EVT_BUTTON,self.listar_pdfs)

        self.button_preparar = wx.Button(self.panel, wx.ID_ANY, 'Preparar', (425, 100),size=(100, 50))
        self.button_preparar.Bind(wx.EVT_BUTTON, self.prepara)

        self.lista_de_pdf = wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE|wx.LIST_STATE_FOCUSED,size=(300,350),pos=(20, 50))      
        self.lista_de_pdf.InsertColumn(0,"PDFs",width=1000)       
        
        self.box_para_print = wx.TextCtrl(self.panel, wx.ID_ANY,"", (350, 200),size=(250, 175),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)

        
        self.frame.Show()
        self.frame.Centre()

    def prepara_trf1est(self,event):
        self.prepara(event='TRF1EST')

    
    def abrir_baixador_trf1(self,event):
        UI_BAIXADOR()
        # os.startfile(os.path.join('A:\\Baixadores\BAIXADOR_TRF1\\baixador_trf1.py'))

    def criar_dia_mes_ano(self,event,data):
        data  = datetime.date(data.GetYear(), data.GetMonth()+1, data.GetDay())
        return data.strftime('%d'),data.strftime('%m'),data.strftime('%Y')
    
    def formar_pasta_de_rotina(self,event,dia,mes,ano,caderno):
        return os.path.join('L:\\', 'rotina', ano, mes, dia, 'download',caderno)

    def printar_na_box(self, event,texto):
        self.box_para_print.AppendText(texto)
        self.box_para_print.AppendText('\n')    
    
    
    def incluir_na_lista(self,event):
        self.lista_de_pdf.InsertStringItem(self.index,event)
        self.index += 1

    def listar_pdfs(self,event):
        self.index = 0
        self.lista_de_pdf.DeleteAllItems()
        self.listar_pdfs_path_download = os.listdir(path_download)
        for pdf in self.listar_pdfs_path_download:
            self.incluir_na_lista(pdf)

    def prepara(self,event):
        data = self.calendario_rotina.GetValue()
        dia,mes,ano = self.criar_dia_mes_ano(event=event,data=data)
        
        if event == 'TRF1EST':
            dlg_pm = wx.MessageDialog(None , "Tudo certo para fazer o PM?","Prepara", wx.YES_NO | wx.ICON_QUESTION)
            result = dlg_pm.ShowModal()
            if result == wx.ID_YES:
                caderno = 'TRF1EST'
                lista_de_pdfs_do_trf1aest = []
                for pdf in self.listar_pdfs_path_download:
                    pdfs_trf1a = re.search(r'^(Caderno(s)*_JUD_)([A-Z]{2}_)', pdf)
                    if pdfs_trf1a:
                        self.printar_na_box(event=event,texto='Caderno: {pdf}'.format(pdf=pdf))
                        lista_de_pdfs_do_trf1aest.append('{path_download}\{pdf}'.format(path_download=path_download,pdf=pdf))

                pdfs_est = ' '.join(lista_de_pdfs_do_trf1aest)
               
                nome_do_pdf = 'PDF_JUNTADO_TRF1AEST.pdf'

                pdf_juntado_trf1a = os.path.join(path_download,nome_do_pdf)
                        
                self.printar_na_box(event=event,texto='Juntando...')
                comando = 'A:\\Baixadores\\JCP\prgs\\sejda-console-3.2.71-bin\\sejda-console-3.2.71\\bin\\sejda-console.bat merge -f {arquivo} -o {padrao_saida}'.format(arquivo=pdfs_est, padrao_saida=pdf_juntado_trf1a)
                if os.system(comando):
                    erro = '############\n Erro ao juntar PDF\n############\n'
                    self.erro_pdftk = erro
                    raise Exception(erro) 

        if event != 'TRF1EST':
            pdf_selec = self.lista_de_pdf.GetFocusedItem()
            nome_do_pdf = self.lista_de_pdf.GetItemText(pdf_selec)
            dic_cadernos = {
                'AC':'ACJF',
                'AM':'AMJF',
                'AP':'APJF',
                'BA':'BAJF',
                'DF':'DFJF',
                'GO':'GOJF',
                'MA':'MAJF',
                'MG':'MGJF',
                'MT':'MTJF',
                'PA':'PAJF',
                'PI':'PIJF',
                'RO':'ROJF',
                'RR':'RRJF',
                'TO':'TOJF',
                'TRF':'TRF1A',
                'TRF1':'TRF1A',
                }

            pdf_do_caderno = re.search(r'^(Caderno(s)*_(JUD|EDT)_)([A-Z1-9]{2,})', nome_do_pdf)
            if pdf_do_caderno:
                caderno = dic_cadernos[pdf_do_caderno.group(4)]
                if caderno == 'TRF1A':
                    lista_de_pdfs_do_trf1a = []
                    
                    for pdf in  self.listar_pdfs_path_download :
                        pdfs_trf1a = re.search(r'^(Caderno(s)*_[a-zA-Z1-9á-úÁ-Ú]{1,}_)TRF', pdf)
                        if pdfs_trf1a:  
                            self.printar_na_box(event=event,texto='{pasta}'.format(pasta=pdf))
                            lista_de_pdfs_do_trf1a.append('{path_download}\{pdf}'.format(path_download=path_download,pdf=pdf))

                    lista_de_pdfs_do_trf1a = sorted(lista_de_pdfs_do_trf1a,reverse=True)
                    pdfs = ' '.join(lista_de_pdfs_do_trf1a)
                    print(pdfs)
                    
                    nome_do_pdf = 'PDF_JUNTADO_TRF1A.pdf'

                    pdf_juntado_trf1a = os.path.join(path_download,nome_do_pdf)
                    
                    self.printar_na_box(event=event,texto='Juntando...')
                    comando = 'A:\\Baixadores\\JCP\prgs\\sejda-console-3.2.71-bin\\sejda-console-3.2.71\\bin\\sejda-console.bat merge -f {arquivo} -o {padrao_saida}'.format(arquivo=pdfs, padrao_saida=pdf_juntado_trf1a)
                    if os.system(comando):
                        erro = '############\n Erro ao juntar PDF\n############\n'
                        self.erro_pdftk = erro
                        raise Exception(erro) 
                        
                    for arq in lista_de_pdfs_do_trf1a:
                        try:
                            os.remove(os.path.join(arq))
                        except:
                            try:
                                shutil.rmtree(os.path.join(arq))
                            except:
                                continue
                
     
        self.printar_na_box(event=event,texto='Caderno: {caderno}'.format(caderno=caderno))
        self.printar_na_box(event=event,texto='Criando pasta de rotina...')
        pasta_de_rotina = self.formar_pasta_de_rotina(event=event,dia=dia,mes=mes,ano=ano,caderno=caderno)
        self.printar_na_box(event=event,texto='{pasta}'.format(pasta=pasta_de_rotina))
        os.makedirs(pasta_de_rotina)
        self.printar_na_box(event=event,texto='Movendo arquivo...')
        pasta_do_pdf = os.path.join(path_download,nome_do_pdf)
        os.rename(pasta_do_pdf, '{pasta_de_rotina}\\{nome_do_pdf}'.format(pasta_de_rotina=pasta_de_rotina,nome_do_pdf='X.pdf'))
        self.listar_pdfs(event=event)
        data_p = self.calendario_p.GetValue()
        dia_p,mes_p,ano_p = self.criar_dia_mes_ano(event=event,data=data_p)
        data_do_p = '{dia_p}/{mes_p}/{ano_p}'.format(dia_p=dia_p,mes_p=mes_p,ano_p=ano_p)
        
        
        self.printar_na_box(event=event,texto='Chamando PM')
        todos_os_comandos = ['A', 'pm {caderno} -d {dia} -m {mes} -a {ano} -p {para_o_dia}'.format(caderno = caderno, dia = dia, mes = mes, ano = ano, para_o_dia = data_do_p)]
        cmd_str = '\n'.join(todos_os_comandos)+'\n'
        p = subprocess.Popen('cmd.exe', shell=True, cwd=r'a:\lido\cmd', stdin=subprocess.PIPE)
        p.stdin.write(cmd_str)
   

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()