#Teste com todas as funcoes em um só arquivo ,
# pois existe um bug para acessar as pastas que 
# eu não estou sabendo resolver :p
from ast import If, Not
from ctypes import Union
from ctypes.wintypes import ATOM
from asyncio import format_helpers
from multiprocessing.sharedctypes import Value
from operator import truediv
from pickle import FALSE, TRUE
from queue import Empty
from re import A
import string
from xmlrpc.client import boolean
import pandas as pd


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

#Função para percorrer os arquivos

##############################################################################

#restricão 1

##############################################################################

#restricão 2

##############################################################################
#(xPI≤42.09,1,p ∨ xPI≤70.62,1,p ∨ xPI≤80.61,1,p ∨ xGS≤37.89,1,n ∨ xGS≤57.55,1,n)
#(xPI≤42.09,2,p ∨ xPI≤70.62,2,p ∨ xPI≤80.61,2,p ∨ xGS≤37.89,2,n ∨ xGS≤57.55,2,n)
#(xPI≤42.09,3,p ∨ xPI≤70.62,3,p ∨ xPI≤80.61,3,p ∨ xGS≤37.89,3,n ∨ xGS≤57.55,3,n)
#(xPI≤42.09,4,p ∨ xPI≤70.62,4,p ∨ xPI≤80.61,4,p ∨ xGS≤37.89,4,n ∨ xGS≤57.55,4,n)
#restricão 3

#def rule3(arquivo):

     # 'a' representa qual o atributo
#    for a in range(length(arquivo)):
        # 'i' representa o numero da regra
#        for i in length():
            # 'j' representa qual o paciente
#            for j in range(length(arquivo)):   
##############################################################################

#restricão 4

##############################################################################

#restricão 5

##############################################################################

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