# Fichier qui permettra de gérer toutes les exécutions du code
import sys
from function import *


# Class Python pour gérer la retranscription dans traces dans un fichier txt
class Tee:
    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, message):
        for output in self.outputs:
            output.write(message)

    def flush(self):
        for output in self.outputs:
            output.flush()



# Sélection du fichier propositions
nom_fichier = "./Propositions/prop-"
print("Veuillez choisir le fichier que vous souhaitez examiner (1-10) ? ")
x = input(">>")
while(0 > int(x) > 11):
    print("Valeur incorrect. Veuillez choisir un nombre compris entre 1 et 10")
    x = input(">>")

fichier = "./Propositions/prop-" + x + ".txt"
fichier_to_write = "trace/trace_" + fichier.split("/")[-1]
print("Ecriture dans", fichier_to_write);
with open(fichier_to_write, "w") as logfile:
    sys.stdout = Tee(sys.__stdout__, logfile)

    # Extraction de la matrice
    n, capacites = lire_matrice_capacite(fichier)

    print(capacites)

    # Affichage de la table des capacités
    print("\nNombre de sommets : " + str(n))
    afficher_matrice(capacites)

    print("Le graphe residuel initial est le graphe de depart.")


    # Si problème de flot max :



    # Si problème de flot min :
    distance = bellman_ford(capacites)
    afficher_cout_plus_court_chemin(distance)




    sys.stdout = sys.__stdout__
