#Teste com todas as funcoes em um só arquivo ,
# pois existe um bug para acessar as pastas que 
# eu não estou sabendo resolver :p
from ast import If, Not
import csv
from ctypes import Union
from ctypes.wintypes import ATOM
from asyncio import format_helpers
from multiprocessing.sharedctypes import Value
from operator import truediv
from pickle import FALSE, TRUE
from queue import Empty
from re import A
import string
import pandas as pd
from xmlrpc.client import boolean
df = pd.read_csv(r'C:\Users\cesar.peixoto\Documents\GitHub\Projeto1-Logica\Arquivos - Pacientes\column_bin_3a_2p.csv') 
#import pandas as pd1
class Formula:
    def __init__(self):
        pass
class Atom(Formula):
    """
    This class represents propositional logic variables.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __hash__(self):
        return hash((self.name, 'atom'))


class Implies(Formula):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2192" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, Implies) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'implies'))


class Not(Formula):

    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def __str__(self):
        return "(" + u"\u00ac" + str(self.inner) + ")"

    def __eq__(self, other):
        return isinstance(other, Not) and other.inner == self.inner

    def __hash__(self):
        return hash((hash(self.inner), 'not'))


class And(Formula):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2227" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, And) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'and'))


class Or(Formula):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2228" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, Or) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'or'))
##############################################################################

def and_all(list_formulas):
    """
    Returns a BIG AND formula from a list of formulas
    For example, if list_formulas is [Atom('1'), Atom('p'), Atom('r')], it returns
    And(And(Atom('1'), Atom('p')), Atom('r')).
    :param list_formulas: a list of formulas
    :return: And formula
    """
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = And(first_formula, formula)
    return first_formula
##############################################################################

def or_all(list_formulas):
    """
    Returns a BIG OR of formulas from a list of formulas.
    For example, if list_formulas is [Atom('1'), Atom('p'), Atom('r')], it returns
    Or(Or(Atom('1'), Atom('p')), Atom('r')).
    :param list_formulas: a list of formulas
    :return: Or formula
    """
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = Or(first_formula, formula)
    return first_formula

##############################################################################

def length(formula):
    """Determines the length of a formula in propositional logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return length(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length(formula.left) + length(formula.right) + 1

##############################################################################

def subformulas(formula):
    """Returns the set of all subformulas of a formula.
    For example, observe the piece of code below.
    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for subformula in subformulas(my_formula):
        print(subformula)
    This piece of code prints p, s, (p v s), (p → (p v s))
    (Note that there is no repetition of p)
    """

    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return {formula}.union(subformulas(formula.inner))
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        sub1 = subformulas(formula.left)
        sub2 = subformulas(formula.right)
        return {formula}.union(sub1).union(sub2)

#  we have shown in class that, for all formula A, len(subformulas(A)) <= length(A).
##############################################################################

# Função para retornar as atomicas de uma formula
def atoms(formula):
    if isinstance(formula,Atom):
        return {formula}
    if isinstance(formula,Not):
        return atoms(formula.inner)
    if isinstance(formula,Implies) or isinstance(formula,Or) or isinstance(formula,And):
        atom1=atoms(formula.left)
        atom2=atoms(formula.right)
        return atom1.union(atom2)
##############################################################################

# Função para verificar se a formula é satisfativel e em qual valoração
def sat_check(formula,atomicas,valoracao):
    if len(atomicas) == 0:
        if truth_value(formula,valoracao):
            return valoracao
        return False
    nova_atomica=atomicas.pop()
    val1= unionDic(valoracao, {nova_atomica: True})
    val2= unionDic(valoracao, {nova_atomica: False})
    result1=sat_check(formula, atomicas.copy(),val1)
    if result1 != False:
        return result1
    return sat_check(formula, atomicas.copy(),val2)
##############################################################################

from enum import Flag
def truth_value(formula, valoracao):
    """Determines the truth value of a formula in an valoracao (valuation).
    An valoracao may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        #para verificar se dentro do dicionario tem um valor para formula.
        if valoracao.__contains__(formula):
            return valoracao[formula] 
        #caso a formula não exista retorna None
        return None
    if isinstance(formula, Not):
        val = truth_value(formula.inner, valoracao)
        return not val
    if isinstance(formula, Implies):
        atom1 = truth_value(formula.left, valoracao)
        atom2 = truth_value(formula.right, valoracao)
        if atom1 is None:
            return None
        if atom1 and not atom2:
            return False
        return True
    if isinstance(formula, And):
        atom1 = truth_value(formula.left, valoracao)
        atom2 = truth_value(formula.right, valoracao)
        if atom1 is None or atom2 is None:
            return None
        if atom1 and atom2:
            return True
        return False
    if isinstance(formula, Or):
        atom1 = truth_value(formula.left, valoracao)
        atom2 = truth_value(formula.right, valoracao)
        if atom1 is None or atom2 is None:
            return None 
        if atom1 or atom2:
            return True
        return False
##############################################################################

# Função de força bruta para satisfatibilidade
def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    atomicas = atoms(formula)
    valoracao = {}
    return sat_check(formula,atomicas,valoracao)
##############################################################################

# União de dicionários
def unionDic(dic1, dic2):
    return (dic1 | dic2)
##############################################################################

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

##############################################################################

#restricão 1
def ret1(arquivo, regra):
  list_row = []
  for atributo in (range(len(arquivo)-1)):
    for i in range(len(regra)):
      if att_check(arquivo[atributo]) in regra[i] :
        if regra[i] == arquivo[atributo]:
          list_row.append(f'X_{arquivo[atributo]}_{str(i+1)}_p')
        elif (regra[i] != arquivo[atributo]):
          list_row.append(f'X_{arquivo[atributo]}_{str(i+1)}_n')
      else:
        list_row.append(f'X_{arquivo[atributo]}_{str(i+1)}_s')  
      
  return list_row 
##############################################################################

#restricão 2
def ret2(arquivo, regra):
  list_row=[]
  for i in (range(len(regra))):
    for a in (range(len(arquivo)-1)):
      if att_check(regra[i]) in arquivo[a]:
        list_row.append(Not(f'X_{arquivo[a]}_{str(i+1)}_s'))
      else:
        list_row.append((f'X_{arquivo[a]}_{str(i+1)}_s'))
  return or_all(list_row)
##############################################################################
#(xPI≤42.09,1,p ∨ xPI≤70.62,1,p ∨ xPI≤80.61,1,p ∨ xGS≤37.89,1,n ∨ xGS≤57.55,1,n)
#(xPI≤42.09,2,p ∨ xPI≤70.62,2,p ∨ xPI≤80.61,2,p ∨ xGS≤37.89,2,n ∨ xGS≤57.55,2,n)
#(xPI≤42.09,3,p ∨ xPI≤70.62,3,p ∨ xPI≤80.61,3,p ∨ xGS≤37.89,3,n ∨ xGS≤57.55,3,n)
#(xPI≤42.09,4,p ∨ xPI≤70.62,4,p ∨ xPI≤80.61,4,p ∨ xGS≤37.89,4,n ∨ xGS≤57.55,4,n)
#restricão 3

def ret3(arquivo,regra):
    list_rows=[]
    for i in range(len(regra)):
            list_atom=[]
            for a in range(len(arquivo)-1):
                    if regra[i] == arquivo[a]:
                        list_atom.append('X_'+str(arquivo[a])+'_'+ str(i+1)+'_'+'p')
                    elif (regra[i] != arquivo[a]):
                        list_atom.append('X_'+str(arquivo[a])+'_'+ str(i+1)+'_'+'n')
                    else:
                        list_atom.append('X_'+str(arquivo[a])+'_'+ str(i+1)+'_'+'s')
            list=or_all(list_atom)
            list_rows.append(list)
    return and_all(list_rows)        
##############################################################################
#(xP I≤42.09,1,p → ¬c1,1) ∧ (xP I≤70.62,1,p → ¬c1,1) ∧ (xP I≤80.61,1,n → ¬c1,1) ∧ (xGS≤37.89,1,p → ¬c1,1 ) ∧ (xGS≤57.55,1,n → ¬c1,1)
#(xP I≤42.09,1,p → ¬c1,2) ∧ (xP I≤70.62,1,p → ¬c1,2) ∧ (xP I≤80.61,1,p → ¬c1,2) ∧ (xGS≤37.89,1,p → ¬c1,2) ∧ (xGS≤57.55,1,p → ¬c1,2)
#(xP I≤42.09,2,p → ¬c2,1) ∧ (xP I≤70.62,2,p → ¬c2,1) ∧ (xP I≤80.61,2,n → ¬c2,1) ∧ (xGS≤37.89,2,p → ¬c2,1 ) ∧ (xGS≤57.55,2,n → ¬c2,1)
#(xP I≤42.09,2,p → ¬c2,2) ∧ (xP I≤70.62,2,p → ¬c2,2) ∧ (xP I≤80.61,2,p → ¬c2,2) ∧ (xGS≤37.89,2,p → ¬c2,2) ∧ (xGS≤57.55,2,p → ¬c2,2)
#(xP I≤42.09,3,p → ¬c3,1) ∧ (xP I≤70.62,3,p → ¬c3,1) ∧ (xP I≤80.61,3,n → ¬c3,1) ∧ (xGS≤37.89,3,p → ¬c3,1 ) ∧ (xGS≤57.55,3,n → ¬c3,1)
#(xP I≤42.09,3,p → ¬c3,2) ∧ (xP I≤70.62,3,p → ¬c3,2) ∧ (xP I≤80.61,3,p → ¬c3,2) ∧ (xGS≤37.89,3,p → ¬c3,2) ∧ (xGS≤57.55,3,p → ¬c3,2)
#(xP I≤42.09,4,p → ¬c4,1) ∧ (xP I≤70.62,4,p → ¬c4,1) ∧ (xP I≤80.61,4,n → ¬c4,1) ∧ (xGS≤37.89,4,p → ¬c4,1 ) ∧ (xGS≤57.55,4,n → ¬c4,1)
#(xP I≤42.09,4,p → ¬c4,2) ∧ (xP I≤70.62,4,p → ¬c4,2) ∧ (xP I≤80.61,4,p → ¬c4,2) ∧ (xGS≤37.89,4,p → ¬c4,2) ∧ (xGS≤57.55,4,p → ¬c4,2
#restricão 4
def ret4(arquivo,regra):
    list_rows=[]
    for i in range(len(regra)):
        for j in range(len(arquivo)):
            list_atom=[]
            for a in range(len(arquivo)-1):
                if (regra[i] == arquivo[a]):
                    list_atom.append(Implies(Atom('X_'+ str(arquivo[a])+'_'+str(i+1)+'_'+'p'),Not(Atom('C'+str(i+1)+'_'+str(j+1)))) ) 
                elif (regra[i] != arquivo[a]):
                    list_atom.append(Implies(Atom('X_'+ str(arquivo[a])+'_'+str(i+1)+'_'+'n'),Not(Atom('C'+str(i+1)+'_'+str(j+1)))) )
                list=and_all(list_atom)
                list_rows.append(list)
    return and_all(list_rows)

##############################################################################
#(c1,1 ∨ c2,1 ∨ c3,1 ∨ c4,1)
#(c1,2 ∨ c2,2 ∨ c3,2 ∨ c4,2)
#restricão 5

def ret5(arquivo,regra):
    list_rows=[]
    for j in range(len(arquivo)):
        list_atom =[]
        for i in range(len(regra)):
            list_atom.append('C_'+str(i+1)+'_'+str(j+1))
        list=or_all(list_atom)
        list_rows.append(list)  
    return and_all(list_rows)
m = [0,1 ]
print(ret3(df.columns,m))
##############################################################################

#Solução
def patologia_solucao(arquivo,regra):
  final_formula= And(
        And(
            And(
                ret1(arquivo,regra),
                ret2(arquivo,regra)
            ),
            And(
                ret3(arquivo,regra),
                ret4(arquivo,regra)
            ),
        ),
        ret5(arquivo,regra)
    )
  solution=(satisfiability_brute_force(final_formula))
  if solution:
    for j in range(len(arquivo)):
      print('Paciente'+ str(j+1)+'tem patologia')
    for i in range(len(regra)):
        for j in range(len(arquivo)):
            list_atom=[]
            for a in range(len(arquivo)):
                if (regra[i] == arquivo[a]):
                    list_atom.append(str(arquivo[0][a]))
    return print(list_atom+'P')
  else:
      print('Paciente'+str(j+1)+'não tem patalogia')

#############################################################################


#############################################################################
#formula1 = Atom('p')  # p
#formula2 = Atom('q')  # q
#formula3 = And(formula1, formula2)  # (p /\ q)
#formula4 = And(Atom('p'), Atom('s'))  # (p /\ s)
#formula5 = Not(And(Atom('p'), Atom('s')))  # (¬(p /\ s))
#formula6 = Or(Not(And(Atom('p'), Atom('s'))), Atom('q'))  # ((¬(p /\ s)) v q)
#formula7 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Atom('r')))  # ((¬(p /\ s)) -> (q /\ r))
#formula8 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s'))))) # ((¬(p /\ s)) -> (q /\ (¬(p /\ s))))
#formula9 = And(formula1, Not(formula1))

#val={
#        Atom('p'): True,
#        Atom('q'): False
#    }

#Testes de funções 
#for atom in atoms(formula1)
#print(atom)
#truth_value(my_formula,val)
#satisfiability_brute_force(formula3)


# with open('C:\Users\Caio\Documents\GitHub\Projeto1-Logica\Arquivos - Pacientes\column_bin_3a_2p.csv', mode='r') as arq:
#     leitor = csv.reader(arq,delimiter=',')
#     linhas = 0
#     for coluna in leitor:
#        if linhas ==0:
#            print(f'Coluna: {"".join(coluna)}')
#            linhas +=1
#        else:
#            print('\tElemento {coluna[0]}')

# csv = pd.reader_csv(r'C:\Users\Caio\Documents\GitHub\Projeto1-Logica\Arquivos - Pacientes\column_bin_3a_2p.csv')
#print(ret5(leitor,3))