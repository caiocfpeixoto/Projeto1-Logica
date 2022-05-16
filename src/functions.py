
from formula import Atom
from formula import Not
from formula import Implies
from formula import Or
from formula import And
from queue import Empty
##############################################################################

# Função para retornar as atomicas de uma formula
def atoms(formula):
    if isinstance(formula,Atom):
        return {formula}
    if isinstance(formula,Not):
        return atoms(formula)
    if isinstance(formula,Implies) or isinstance(formula,Or) or isinstance(formula,And):
        atom1 = atoms(formula.left) 
        atom2 = atoms(formula.right)
        return (atom1).union(atom2)
##############################################################################
    
# Função para retornar a valoração em que a formula fica 'true'
def true_value(formula,valoracao):
    if isinstance(formula,Atom):
        if valoracao(formula)==True:
            return True
        return False
    if isinstance(formula,Not):
        return Not(true_value(formula))
    if isinstance(formula,Implies):
        return Implies(true_value(formula.left),true_value(formula.right))
    if isinstance(formula,Or):
        return Or(true_value(formula.left),true_value(formula.right))
    if isinstance(formula,And):
        return And(true_value(formula.left),true_value(formula.right))
##############################################################################

# Função para retornar se a formula é satisfatível 
def sat_check(formula,atom,valoracao):
    if atom is Empty :
        if true_value(formula,valoracao)==True :
            return valoracao
        return False
    atom=atom.pop()
    val1 = valoracao.union(atom,True)
    val2 = valoracao.union(atom,False)
    result1=sat_check(formula,atom,val1)
    if result1 != False:
        return result1
    return sat_check(formula,atom,val2)
##############################################################################

# Função ded força bruta para satisfatibilidade
#atom=atoms(formula)
##############################################################################

my_formula = Implies(Or(Atom('p'),Atom('q')),Or(Atom('r'),Atom('s')))
# p v q --> r v s
for atom in atoms(my_formula):
    print(atom)    