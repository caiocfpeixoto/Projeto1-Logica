import os
from sre_constants import AT
import pandas as pd
from ferramentas.semantics import *


#altere o endereço de acordo com localização do arquivo
#usar o df como padrão
df = pd.read_csv(r'C:\\Users\Luciano\Desktop\Workspace\Python\Projeto I\\Arquivos - Pacientes\column_bin_5a_3p.csv')  
#regra3a_2p  {['PI > 54.92]'}
#regra3a_3p  {['PI > 70.62','GS > 57.55']}o número é definido pelos atributos diferentes
#regra3a_4p ['PI > 42.09', 'LA > 39.63', 'GS > 37.89'] tem algo de errado com a regra, talvez ajude na modelagem
# regra1 = ['PI > 54.92']
# regra2 = ['PI > 70.62', 'GS > 57.55']
# regra3 = ['PI > 42.09', 'LA > 39.63', 'GS > 37.89']

sem_patologia=df[df["P"]!=1]  #pacientes sem patologia

com_patologia=df[df["P"]==1]  #pacientes com patologia

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
  #if :
  
  return m

#def pato(arquivo):
  #for a in range(len(arquivo)):

#(X_a_i_p) V (X_a_i_n) V (X_a_i_s)
#df.columns é o se utiliza pra contar as chaves(ex=PI > x) das colunas
def ret1(arquivo, regra):
  list_row = []
  for i in range(regra):  
    list_atoms = []
    for a in (range(len(arquivo)-1)):
      list_atom=[]
      for aux in range(3):
        list_aux = []
        if aux == 0:
          list_aux.append(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_p'))
          list_aux.append(Not(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_n')))
          list_aux.append(Not(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_s')))
          
          
        if aux == 1:
          list_aux.append(Not(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_p')))
          list_aux.append(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_n'))
          list_aux.append(Not(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_s')))
            
        if aux == 2:
          list_aux.append(Not(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_p')))
          list_aux.append(Not(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_n')))
          list_aux.append(Atom('X_'+arquivo[a]+'_'+str(i+1)+'_s'))
        
        list = and_all(list_aux) 
        list_atom.append(list)
        
      list = or_all(list_atom) 
      list_atoms.append(list)

    list = and_all(list_atoms)
    list_row.append(list)  

  return and_all(list_row)


# (¬xP I≤42.09,1,s V ¬xP I≤70.62,1,s V ¬xP I≤80.61,1,s V ¬xGS≤37.89,1,s V ¬xGS≤57.55,1,s)
# (¬xP I≤42.09,2,s V ¬xP I≤70.62,2,s V ¬xP I≤80.61,2,s V ¬xGS≤37.89,2,s V ¬xGS≤57.55,2,s)
# (¬xP I≤42.09,3,s V ¬xP I≤70.62,3,s V ¬xP I≤80.61,3,s V ¬xGS≤37.89,3,s V ¬xGS≤57.55,3,s)
# (¬xP I≤42.09,4,s V¬xP I≤70.62,4,s V ¬xP I≤80.61,4,s V ¬xGS≤37.89,4,s V ¬xGS≤57.55,4,s)

#df.columns é o se utiliza pra contar as chaves(ex=PI > x) das colunas
def ret2(arquivo, regra):
  list_row=[]
  for i in (range(regra)):
    list_atom = []
    for a in (range(len(arquivo)-1)):
      list_atom.append(Not(Atom(f'X_{arquivo[a]}_{str(i+1)}_s')))
    list = or_all(list_atom)
    list_row.append(list)
  
  return and_all(list_row)     

 #leitura da parte de 1 e 0 dos pacientes
# for linha in range(len(df.index)):
#      for coluna in range(len(df.columns)-1) :
#          if df.iloc[linha][coluna] == 1:
#            print(f'1 = {df.iloc[linha][coluna]}')
#          if df.iloc[linha][coluna] != 1:
#            print(f'0 = {df.iloc[linha][coluna]}')    

def ret3(arquivo,regra):
  list_rows=[]
  for i in range(regra):
    for linha in range(len(arquivo.index)):
      list_atom=[]
      for coluna in  range(len(arquivo.columns)-1):  
        if arquivo.iloc[linha,coluna] == 1:
          list_atom.append(Atom('X_'+str(arquivo.columns[coluna])+'_'+(str(i+1))+'_n'))
        else:
          list_atom.append(Atom('X_'+str(arquivo.columns[coluna])+'_'+(str(i+1))+'_p'))  
      list=or_all(list_atom)
    list_rows.append(list)
  return and_all(list_rows)

def ret4(arquivo,regra):
    list_rows=[]
    for i in range(regra):
        for linha in range(len(arquivo.index)):
            list_atom=[]
            for coluna in range(len(arquivo.columns)-1):
                if (arquivo.iloc[linha,coluna] == 1):
                    list_atom.append(Implies(Atom('X'+ str(arquivo.columns[coluna])+''+str(i+1)+''+'n'),Not(Atom('C'+str(i+1)+'_'+str(linha+1)))) ) 
                else:
                    list_atom.append(Implies(Atom('X'+ str(arquivo.columns[coluna])+''+str(i+1)+''+'p'),Not(Atom('C'+str(i+1)+'_'+str(linha+1)))) )
                list=and_all(list_atom)
                list_rows.append(list)
    return and_all(list_rows)

def ret5(arquivo, regra):
    list_rows=[]
    for j in range(len(arquivo.index)):
        list_atom =[]
        for i in range(regra):
            list_atom.append(Atom('C'+str(i+1)+'_'+str(j+1)))
        list=or_all(list_atom)
        list_rows.append(list)
    return and_all(list_rows)

def patologia_solucao(arquivo, regra):
  arquivo_sem_patologia=arquivo[arquivo["P"]!=1]  #pacientes sem patologia
  arquivo_com_patologia=arquivo[arquivo["P"]==1]  #pacientes com patologia

  final_formula= And(
    And(
      And(
          ret1(arquivo.columns,regra),
          ret2(arquivo.columns,regra)
        ),
      And(
          ret3(arquivo_sem_patologia,regra),
          ret4(arquivo_com_patologia,regra)
        ),
         ),
      ret5(arquivo_com_patologia,regra)
    )
  solution=(satisfiability_brute_force(final_formula))
  return solution
 

# def patologia_solucao(arquivo_ret1_e_ret2, arquivo_ret3, arquivo_ret4_e_ret5, regra):
#   final_formula= And(
#         And(
#           And(
#             ret1(arquivo_ret1_e_ret2,regra),
#             ret2(arquivo_ret1_e_ret2,regra)
#              ),
#           And(
#             ret3(arquivo_ret3,regra),
#             ret4(arquivo_ret4_e_ret5,regra)
#             ),
#         ),
#         ret5(arquivo_ret4_e_ret5,regra)
#      )
#   solution=(satisfiability_brute_force(final_formula))




               




