from enum import Flag
from base.formula import *
from ferramentas.functions import atoms
from ferramentas.functions import sat_check

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
        if val is None:
            return None
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