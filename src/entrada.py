import os
from sre_constants import AT
import pandas as pd
from ferramentas.semantics import *


#altere o endereço de acordo com localização do arquivo
#usar o df como padrão
df = pd.read_csv(r'C:\\Users\Luciano\Desktop\Workspace\Python\Projeto I\\Arquivos - Pacientes\column_bin_3a_2p.csv')  
#regra3a_2p  {['PI > 54.92]'}
#regra3a_3p  {['PI > 70.62','GS > 57.55']}
#regra3a_4p ['PI > 42.09', 'LA > 39.63', 'GS > 37.89'] tem algo de errado com a regra, talvez ajude na modelagem
regra1 = ['PI > 54.92']
regra2 = ['PI > 70.62', 'GS > 57.55']

#print(df)

#Checagem na situação em que a não está em i
def att_check(arquivo):
  if 'PI' in arquivo:
    #print(f'PI está presente -> {arquivo[n]}')
    check = 'PI'
   
  if 'GS' in arquivo:
    #print(f'GS está presente -> {arquivo[n]}') 
    check = 'GS'

  if 'PT' in arquivo:
     #print(f'PT está presente -> {arquivo[n]}')  
    check = 'PT'

  if 'LA' in arquivo:
    #print(f'LA está presente -> {arquivo[n]}')
    check = 'LA'

  if 'SS' in arquivo:
    #print(f'SS está presente -> {arquivo[n]}')
    check = 'SS'

  if 'RP' in arquivo:
    #print(f'RP está presente -> {arquivo[n]}')  
    check = 'RP'
  
  return check   

#(X_a_i_p) V (X_a_i_n) V (X_a_i_s)
#df.columns é o se utiliza pra contar as chaves(ex=PI > x) das colunas
def ret1(arquivo, regra):
  list_row = []
  for a in (range(len(arquivo)-1)):
    for i in range(len(regra)):
      if att_check(arquivo[a]) in regra[i] :
        if regra[i] == arquivo[a]:
          list_row.append(f'X_{arquivo[a]}_{str(i+1)}_p')
        elif (regra[i] != arquivo[a]):
          list_row.append(f'X_{arquivo[a]}_{str(i+1)}_n')
      else:
        list_row.append(f'X_{arquivo[a]}_{str(i+1)}_s')  
      
  return list_row

'''
(¬xP I≤42.09,1,s V ¬xP I≤70.62,1,s V ¬xP I≤80.61,1,s V ¬xGS≤37.89,1,s V ¬xGS≤57.55,1,s)
(¬xP I≤42.09,2,s V ¬xP I≤70.62,2,s V ¬xP I≤80.61,2,s V ¬xGS≤37.89,2,s V ¬xGS≤57.55,2,s)
(¬xP I≤42.09,3,s V ¬xP I≤70.62,3,s V ¬xP I≤80.61,3,s V ¬xGS≤37.89,3,s V ¬xGS≤57.55,3,s)
(¬xP I≤42.09,4,s V¬xP I≤70.62,4,s V ¬xP I≤80.61,4,s V ¬xGS≤37.89,4,s V ¬xGS≤57.55,4,s)
'''
#df.columns é o se utiliza pra contar as chaves(ex=PI > x) das colunas
def ret2(arquivo, regra):
  list_row=[]
  for i in (range(len(regra))):
    for a in (range(len(arquivo)-1)):
      if att_check(regra[i]) in arquivo[a]:
        list_row.append(f'notX_{arquivo[a]}_{str(i+1)}_s')
      else:
        list_row.append(f'X_{arquivo[a]}_{str(i+1)}_s')
  return list_row      

'''
def ret3(arquivo,regra):
    list_rows=[]
    for i in range(len(regra)):
            list_atom=[]
            for a in range(len(arquivo)-1):  
                list_atom.append('X'+str(arquivo[0][a])+'_'+ str(i+1)+'_'+ str())
            list=or_all(list_atom)
            list_rows.append(list)
    return and_all(list_rows)  

def ret4(arquivo,regra):
    list_rows=[]
    for i in range(len(regra)):
        for j in range(len(arquivo)):
            list_atom=[]
            for a in range(len(arquivo)-1):
                list_atom.append(Implies(Atom('X'+ str(arquivo[0][a])+'_'+str(i+1)+'_',),Not(Atom('C'+str(i+1)+'_'+str(j+1)))) )
                list=and_all(list_atom)
                list_rows.append(list)
    return and_all(list_rows)

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
'''


               




