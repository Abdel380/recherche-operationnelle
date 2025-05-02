from function import *
from complexite import*

n, capacites, couts = lire_matrice_capacite_et_cout("./Propositions/prop-11.txt")

flot_total, cout_total = flot_a_cout_minimal(couts, capacites, 4)
