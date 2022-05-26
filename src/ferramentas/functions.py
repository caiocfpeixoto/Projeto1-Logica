
from asyncio import format_helpers
from multiprocessing.sharedctypes import Value
from operator import truediv
from pickle import FALSE, TRUE
from queue import Empty
from ferramentas.semantics import *
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

# Função para retornar se a formula é satisfatível 
def sat_check(formula,atomicas,valoracao):
    if atomicas is Empty :
        if truth_value(formula,valoracao)==True :
            return valoracao
        return False
    nova_atomica=atomicas.pop()
    val1 = valoracao.union({atomicas,True})
    val2 = valoracao.union({atomicas,False})
    result1=sat_check(formula,atomicas,val1)
    if result1 != False:
        return result1
    return sat_check(formula,atomicas,val2)

##############################################################################
