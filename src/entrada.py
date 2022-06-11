import os
from sre_constants import AT
import pandas as pd
from ferramentas.semantics import *


#altere o endereço de acordo com localização do arquivo
#usar o df como padrão
df = pd.read_csv(r'C:\\Users\Luciano\Desktop\Workspace\Python\Projeto I\\Arquivos - Pacientes\column_bin_3a_2p.csv')  
#regra3a_2p  {['PI > 54.92]'}
#regra3a_3p  {['PI > 70.62','GS > 57.55']}o número é definido pelos atributos diferentes
#regra3a_4p ['PI > 42.09', 'LA > 39.63', 'GS > 37.89'] tem algo de errado com a regra, talvez ajude na modelagem
regra1 = ['PI > 54.92']
regra2 = ['PI > 70.62', 'GS > 57.55']
regra3 = ['PI > 42.09', 'LA > 39.63', 'GS > 37.89']

#print(df)

#Conta as regras
#m = contagem(df.columns)
def contagem(arquivo):
  list = [0, 0, 0, 0, 0, 0]
  m = 0
  for a in range(len(arquivo)):
    if 'PI' in arquivo[a]:
      if list[0] == 0:
        m += 1
        list[0] += 1
    if 'GS' in arquivo[a]:
      if list[1] == 0:
        m += 1
        list[1] += 1
    if 'PT' in arquivo[a]:
      if list[2] == 0:
        m += 1 
        list[2] += 1  
    if 'LA' in arquivo[a]:
      if list[3] == 0:
        m += 1
        list[3] += 1
    if 'SS' in arquivo[a]:
      if list[4] == 0:
        m += 1  
        list[4] += 1
    if 'RP' in arquivo[a]:
      if list[5] == 0:
        m += 1 
        list[5] += 1 

  return m

#(X_a_i_p) V (X_a_i_n) V (X_a_i_s)
#df.columns é o se utiliza pra contar as chaves(ex=PI > x) das colunas
def ret1(arquivo, regra):
  list_row = []
  for i in range(len(regra)):  
    list_atoms = []
    for a in (range(len(arquivo)-1)):
      list_atom=[]
      for aux in range(3):
        list_aux = []
        if aux == 0:
          list_aux.append(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_p'))
          list_aux.append(Not('X_'+arquivo[a]+'_'+str(i+1)+'_n'))
          list_aux.append(Not('X_'+arquivo[a]+'_'+str(i+1)+'_s'))
          
          
        if aux == 1:
          list_aux.append(Not('X_'+arquivo[a]+'_'+str(i+1)+'_p'))
          list_aux.append(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_n'))
          list_aux.append(Not('X_'+arquivo[a]+'_'+str(i+1)+'_s'))
            
        if aux == 2:
          list_aux.append(Not('X_'+arquivo[a]+'_'+str(i+1)+'_p'))
          list_aux.append(Not('X_'+arquivo[a]+'_'+str(i+1)+'_n'))
          list_aux.append(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_s'))
        
        list = and_all(list_aux) 
        list_atom.append(list)
        
      list = or_all(list_atom) 
      list_atoms.append(list)

    list = and_all(list_atoms)
    list_row.append(list)  

  return and_all(list_row)

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
    list_atom = []
    for a in (range(len(arquivo)-1)):
      list_atom.append(Not(f'X_{arquivo[a]}_{str(i+1)}_s'))
    list = or_all(list_atom)
    list_row.append(list)
  
  return and_all(list_row)       

def ret3(arquivo,regra):
    list_atoms=[]
    for i in range(len(regra)):
            list_atom=[]
            for a in range(len(arquivo)-1):  
                list_atom.append('X'+str(arquivo[0][a])+'_'+ str(i+1)+'_'+ str())
            list=or_all(list_atom)
            list_atoms.append(list)
    return and_all(list_atoms)  

def ret4(arquivo,regra):
    list_atoms=[]
    for i in range(len(regra)):
        for j in range(len(arquivo)):
            list_atom=[]
            for a in range(len(arquivo)-1):
                list_atom.append(Implies(Atom('X'+ str(arquivo[0][a])+'_'+str(i+1)+'_',),Not(Atom('C'+str(i+1)+'_'+str(j+1)))) )
                list=and_all(list_atom)
                list_atoms.append(list)
    return and_all(list_atoms)

def ret5(arquivo,regra):
    list_atoms=[]
    for j in range(len(arquivo)):
      list_atom =[]
      for i in range(len(regra)):
        list_atom.append('C'+str(i+1)+''+str(j+1))
      list=or_all(list_atom)
      list_atoms.append(list)
    return and_all(list_atoms)

#arquivo=[1,0,1],[0,0,0]
#m=[0,1,2,3]
#print(ret5(arquivo,m))



               




