import os
import string
import random
import numpy as np
from operator import add

#-----------------------------------------------------------------------------------

NUMERO_DE_GRUPOS=1
DIRETORIO_SAIDA = "/scratch/prjeeesd/marcio.sorgato/teste/grupos"

DIRETORIOS_CASOS = ["/scratch/prjeeesd/marcio.sorgato/teste/tip6"]

#-----------------------------------------------------------------------------------

def lista_diretorios_do_caminho(path):
  print("\nlista_diretorios_do_caminho("+path+")")
  diretorios = []
  for x in os.listdir(path):
    diretorio = os.path.join(path, x)
    if os.path.isdir(diretorio) and x[0] == 'c':
      diretorios.append(diretorio)
      print("\t"+diretorio)
  return diretorios

#-----------------------------------------------------------------------------------  

def dividir_em_grupos(_list):
  print("dividir_em_grupos(): tamnhoLista = "+str(len(_list)))
  np_array = np.array(_list)
  sublists = np.array_split(np_array, NUMERO_DE_GRUPOS)
  sublists = [list(x) for x in sublists]
  return sublists

#-----------------------------------------------------------------------------------
  
#gerar lista de casos por tipologia = [[caminho_tip1_caso1, caminho_tip1_caso2], [caminho_tip2_caso1, caminho_tip2_caso2]]
lista_casos_tipologias = []
for d in DIRETORIOS_CASOS:
  lista_casos = lista_diretorios_do_caminho(d)
  lista_casos_tipologias.append(lista_casos)

# dividir em N grupos = [[[caminho_tip1_caso1], [caminho_tip1_caso2]], [[caminho_tip2_caso1], [caminho_tip2_caso2]]]
grupos_tipologias = []
for lista_casos_tipologia in lista_casos_tipologias:
  lista_casos_tipologia = dividir_em_grupos(lista_casos_tipologia)
  grupos_tipologias.append(lista_casos_tipologia)

# mesclar grupos
grupos_mesclados = grupos_tipologias[0]
for grupos_tipologia in grupos_tipologias[1:]:
  grupos_mesclados = map(add, grupos_mesclados, grupos_tipologia)
  

# gerar arquivos dos grupos
i=0
for grupo in grupos_mesclados:
  i = i + 1
  nome_arquivo = 'grupo_{0:0>3d}'.format(i)
  group_file_path = os.path.join(DIRETORIO_SAIDA, nome_arquivo)
  with open(group_file_path, 'w+') as group_file:
    for caso in grupo:
      group_file.write(caso+os.linesep)


  
