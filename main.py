from function import *

n,capacites =lire_matrice_capacite("./Propositions/prop-1.txt")
print(initialiser_flots_excedents_source(n, capacites))

print(voisins_par_sommet_complet(capacites))

flots, hauteurs, excedents = initialiser_flots_excedents_source(n, capacites)

# Afficher les initialisations
print("Flots initiaux:", flots)
print("Hauteurs initiaux:", hauteurs)
print("Excédents initiaux:", excedents)

# Test de la fonction 'pousser' : pousser du flot de s vers a
u, v = 0, 1  # s → a
print("\nAvant d'appliquer 'pousser' (s → a) :")
print("Flots:", flots)
print("Excédents:", excedents)
pousser(u, v, excedents, hauteurs, capacites, flots)
print("\nAprès avoir appliqué 'pousser' (s → a) :")
print("Flots:", flots)
print("Excédents:", excedents)

# Test de la fonction 'reetiqueter' pour un sommet (ici 'a')
print("\nAvant d'appliquer 'reetiqueter' pour 'a' :")
print("Hauteurs:", hauteurs)
reetiqueter(1, excedents, hauteurs, capacites, flots)
print("\nAprès avoir appliqué 'reetiqueter' pour 'a' :")
print("Hauteurs:", hauteurs)

