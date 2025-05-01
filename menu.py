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


def menu():
    run = True


    while run: # Debut du code Tant que l'utilisateur veut tester un probleme de flot
        # Sélection du fichier propositions
        nom_fichier = "./Propositions/prop-"
        print("Veuillez choisir le fichier que vous souhaitez examiner (1-10) ? ")
        x = input(">> ")
        while(0 > int(x) > 11):
            print("Valeur incorrect. Veuillez choisir un nombre compris entre 1 et 10")
            x = input(">> ")
        algorithme = "MIN"
        if (int(x) < 6):
            print(f"Veuillez choisir l'algorithme que vous souhaitez utiliser pour examiner la proposition {x}, probleme de flot max\n\t1. Ford-Fulkerson\n\t2. Pousser-reetiqueter")
            algo = input(">> ")
            while(algo != "1" and algo != "2"):
                print("Saisi incorrect, saisissez 1 ou 2")
                algo = input(">> ")
            if (algo == "1"):
                algorithme = "FF"
            else:
                algorithme ="PR"

        fichier = "./Propositions/prop-" + x  + ".txt"
        fichier_to_write = "trace/E1-trace" + x + "-" + algorithme + ".txt"
        print("Ecriture dans", fichier_to_write);
        with open(fichier_to_write, "w") as logfile:
            sys.stdout = Tee(sys.__stdout__, logfile)

            # Extraction de la matrice
            n, capacites = lire_matrice_capacite(fichier)

            # Affichage de la table des capacités
            print("\nNombre de sommets : " + str(n))
            afficher_matrice(capacites)

            print("Le graphe residuel initial est le graphe de depart.")


            # Si problème de flot max :
            if (algorithme == "FF"):
                edmonds_karp(n, capacites)

            elif (algorithme == "PR"):
                pousser_reetiqueter(capacites, n)

            # Si problème de flot min :
            else:
                n, capacites, couts = lire_matrice_capacite_et_cout(fichier)

                print("Veuillez choisir la valeur de flot que vous souhaitez envoyer ")
                valeur_flot = input(">> ")
                flot_total, cout_total = flot_a_cout_minimal(couts, capacites, int(valeur_flot))

            # Fin de l'écriture dans un txt
            sys.stdout = sys.__stdout__



        print("\nVoulez-vous tester un autre probleme de flot (oui/non) ? ")
        continuer = input(">> ")
        while(continuer not in ["oui","non"]):
            print("\nSaisi incorrect ! Choisissez oui ou non ")
            continuer = input(">> ")
        if continuer == "non":
            run = False


if __name__ == '__main__':
    menu()