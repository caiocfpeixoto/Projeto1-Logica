
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



##############################################################################

# Função para verificar se a formula é satisfativel e em qual valoração
def sat_check(formula,atomicas,valoracao):
    if len(atomicas) == 0:
        if truth_value(formula,valoracao):
            return valoracao
        return False
    nova_atomica=atomicas.pop()
    val1= unionDic(valoracao, {nova_atomica.name: True})
    val2= unionDic(valoracao, {nova_atomica.name: False})
    result1=sat_check(formula, atomicas.copy(),val1)
    if result1 != False:
        return result1
    return sat_check(formula, atomicas.copy(),val2)
##############################################################################

# União de dicionários
def unionDic(dic1, dic2):
    return (dic1 | dic2)