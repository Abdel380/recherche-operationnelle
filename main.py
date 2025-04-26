from function import *

# Lecture du fichier contenant capacités et coûts
n, capacites, couts = lire_matrice_capacite_et_cout("./Propositions/prop-10.txt")


distances, predecesseurs = bellman_ford_avec_predecesseurs(couts, 0)
print(predecesseurs)

chemin = reconstruire_chemin(predecesseurs, n-1)
afficher_chemin_cout_et_capacite(chemin, couts, capacites)