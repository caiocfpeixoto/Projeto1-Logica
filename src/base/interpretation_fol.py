from base.fol_formula import *
from base.term import *
 
class Interpretation:
    def __init__(self, domain, predicates, functions, constants, variables):
        self.domain = domain
        self.predicates = predicates
        self.functions = functions
        self.constants = constants
        self.variables = variables
    
    def interpretation_term(self, term):
        """Returns the the interpretation of term in a interpretation.
        For example, let interpretation1 be the interpretation defined in the first lines of this file.
        interpretation1.interpretation_term(Fun('g', [Fun('f', [Var('x'), Con('a')])]))
        must return 2
        """
        pass

    def truth_value(self, formula):
        """Returns the the truth-value of an input first-order formula in a interpretation."""
        pass