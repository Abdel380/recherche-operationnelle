from function import *

n,capacites =lire_matrice_capacite("./Propositions/prop-1.txt")

flots,hauteurs,excedents = initialiser_flots_excedents_source(n,capacites)
etiquettes = generer_etiquettes(n)



print(pousser_reetiqueter(capacites,n))

