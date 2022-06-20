from enum import Flag
from base.formula import *


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
        return (atom1).union(atom2)
##############################################################################
def truth_value(formula, valoracao):
    """Determines the truth value of a formula in an valoracao (valuation).
    An valoracao may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        #para verificar se dentro do dicionario tem um valor para formula.
        if valoracao.__contains__(formula.name):
            return valoracao[formula.name] 
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

# Função ded força bruta para satisfatibilidade
def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    atomicas = atoms(formula)
    valoracao = {}
    return sat_check(formula,atomicas,valoracao)
###############################################################################    
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