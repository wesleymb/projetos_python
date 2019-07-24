import os
import re
import argparse

def criar_caderno_por_intervalos(caderno,intervalos,novo_caderno):
    lista_de_intervalos = []
    lista_de_linhas = []
    with open (intervalos,'r') as dados_intervalo:
        linhas_do_intervalo = dados_intervalo.readlines()
        for linha_do_intervalo in linhas_do_intervalo:
            linha_para_buscar = re.search(r'(^[0-9]{1,})(\:)', linha_do_intervalo)
           
            if linha_para_buscar:
                lista_de_linhas.append(linha_para_buscar.group(1))
                if len(lista_de_linhas) == 2:
                    lista_de_intervalos.append(lista_de_linhas)
                    lista_de_linhas = []


    linhas_do_caderno_novo = []
    print(lista_de_intervalos)
    for intervalo in lista_de_intervalos:
        for i in range(int(intervalo[0]),int(intervalo[-1])+1):
            if 0 not in linhas_do_caderno_novo or i == 0:
                linhas_do_caderno_novo.append(0)
            linhas_do_caderno_novo.append(i-1)
    
    linhas_copiada_do_original = []
    linha_final = None
    with open (caderno,'r') as dados_caderno:
        linhas_de_caderno = dados_caderno.readlines()
        for numero_da_linha in linhas_do_caderno_novo:
            linhas_copiada_do_original.append(linhas_de_caderno[numero_da_linha])
            linha_final = linhas_de_caderno[-1]
        
    
    with open ('C:\\tmp\\{}'.format(novo_caderno),'w') as caderno_novo:
            caderno_novo.writelines(linhas_copiada_do_original)
            if linha_final not in linhas_copiada_do_original:
                caderno_novo.write(linha_final)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--dia",      dest='caderno',         type=str,      help="NNX original")
    parser.add_argument("-i", "--mes",      dest='intervalos',         type=str,    help='Arquivo txt')
    parser.add_argument("-nc", "--ano",      dest='novo_caderno',         type=str,     help='Nome do caderno')
    args = parser.parse_args()
    args.novo_caderno = args.novo_caderno.upper()
    
    print('Origem: {}'.format(args.caderno))
    print('Arquivo de intervalos: {}'.format(args.intervalos))
    print('Nome do novo caderno: {novo_caderno}'.format(novo_caderno=args.novo_caderno))
    criar_caderno_por_intervalos(caderno=args.caderno,intervalos=args.intervalos,novo_caderno='{novo_caderno}.nnx'.format(novo_caderno=args.novo_caderno))