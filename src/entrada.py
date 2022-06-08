import os
import pandas as pd
from ferramentas.semantics import *


  #altere o endereço de acordo com localização do arquivo
df = pd.read_csv(r'C:\\Users\Luciano\Desktop\Workspace\Python\Projeto I\\Arquivos - Pacientes\column_bin_3a_2p.csv')  



print(df)
"""
def pegar_comparador(arquivo):
    tabela = []
    for linha in range(len(arquivo)):
        for coluna in range(len(arquivo)):
            if coluna != 'P':
                tabela = arquivo[0][coluna]
    return tabela
"""
#def ret1(arquivo):

def ret5(arquivo,regra):
    list_rows=[]
    for j in range(len(arquivo)):
      list_atom =[]
      for i in range(len(regra)):
        list_atom.append('C'+str(i+1)+''+str(j+1))
      list=or_all(list_atom)
      list_rows.append(list)
    return and_all(list_rows)
arquivo=[1,0,1],[0,0,0]
m=[0,1,2,3]
print(ret5(arquivo,m))


               




