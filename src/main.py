from base.formula import *
from ferramentas.functions import *
from ferramentas.semantics import *


formula1 = Atom('p')  # p
formula2 = Atom('q')  # q
formula3 = And(formula1, formula2)  # (p /\ q)
formula4 = And(Atom('p'), Atom('s'))  # (p /\ s)
formula5 = Not(And(Atom('p'), Atom('s')))  # (¬(p /\ s))
formula6 = Or(Not(And(Atom('p'), Atom('s'))), Atom('q'))  # ((¬(p /\ s)) v q)
formula7 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Atom('r')))  # ((¬(p /\ s)) -> (q /\ r))
formula8 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s'))))) # ((¬(p /\ s)) -> (q /\ (¬(p /\ s))))
formula9 = And(formula1, Not(formula1))
    

val={
        Atom('p'): True,
        Atom('q'): False
    }



def main():
    truth_value(formula1,val)

if __name__ == "__main__":
  main()