# Fichier qui permettra de gérer toutes les exécutions du code
import sys
import os
from function import *
from complexite import *


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


def fichier_valide(csv_path):
    if not os.path.exists(csv_path):
        print(f"Le fichier {csv_path} n'existe pas.")
        return False

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            if not any(reader):  # Si le fichier est vide après l'en-tête
                print(f"Le fichier {csv_path} est vide.")
                return False
    except StopIteration:
        print(f"Le fichier {csv_path} est vide ou mal formaté.")
        return False

    return True


def effacer_csv():
    fichiers = [
        "./temps_execution/temps_execution_FF.csv",
        "./temps_execution/temps_execution_PR.csv",
        "./temps_execution/temps_execution_FM.csv",
    ]

    for fichier in fichiers:
        if os.path.exists(fichier):
            with open(fichier, 'w', newline='', encoding='utf-8') as f:
                pass
            print(f"Le fichier {fichier} a été vidé.")
        else:
            print(f"Le fichier {fichier} n'existe pas.")



def analyse_complexite():
    print("Voulez-vous essayer la complexité sur un graphe aléatoire ? (oui/non)")
    n = input(">> ").lower()
    while n != "oui" and n != "non":
        print("Réponse incorrecte. Veuillez répondre par oui ou non.")
        n = input(">> ").lower()
    if n == "oui":
        print(
            "Combien de sommet voulez-vous dans votre réseau de flot ? Veuillez sélectionner un nombre entier positif.")
        y = int(input(">> "))
        while 0 > y:
            print("Valeur incorrecte. Veuillez choisir un nombre entier positif.")
            y = int(input(">> "))
        nuage_de_points(y)

def affichage_complexite():
    print("Voulez-vous afficher la complexité de l'un des algorithme?(oui/non)")
    afficher_complexite = input(">> ").lower()
    if afficher_complexite != "oui" and afficher_complexite != "non":
        print("Réponse incorrecte. Veuillez répondre par oui ou non.")
        print("Voulez-vous afficher la complexité de l'un des algorithmes ?(oui/non)")
        afficher_complexite = input(">> ").lower()

    if afficher_complexite == "oui":
        marche = True
        while marche:
            print("Quel algorithme voulez-vous afficher ?(FF, PR, FM) ")
            algorithme = input(">> ").lower()
            while algorithme not in ["ff", "pr", "fm"]:
                print("Cet algorithme n'existe pas. Veuillez entrer 'FF', 'PR', 'FM'.")
                algorithme = input(">> ").lower()

            print(f"Complexité de l'algorithme {algorithme}")
            if algorithme == "ff":
                plot_algorithm("./temps_execution/temps_execution_FF.csv", "FF")
            elif algorithme == "pr":
                plot_algorithm("./temps_execution/temps_execution_PR.csv", "PR")
            elif algorithme == "fm":
                plot_algorithm("./temps_execution/temps_execution_FM.csv", "FM")

            print("Voulez-vous afficher la complexité d'un autre algorithme ?(oui/non)")
            a = input(">> ").lower()

            while a != "oui" and a != "non":
                print("Réponse incorrecte. Veuillez répondre par oui ou non.")
                a = input(">> ").lower()

            if a == "non":
                marche = False
            else:
                print("Revenir à la sélection des flots. ")


def analyse_flot():
    print("Veuillez choisir le fichier que vous souhaitez examiner (1-10) ? ")
    x = input(">> ")
    while 0 > int(x) > 11:
        print("Valeur incorrecte. Veuillez choisir un nombre compris entre 1 et 10")
        x = input(">> ")

    algorithme = "MIN"
    if int(x) < 6:
        print(
            f"Veuillez choisir l'algorithme que vous souhaitez utiliser pour examiner la proposition {x}, problème de flot max\n\t1. Ford-Fulkerson\n\t2. Pousser-reetiqueter")
        algo = input(">> ")
        while algo != "1" and algo != "2":
            print("Saisi incorrect, saisissez 1 ou 2")
            algo = input(">> ")
        if algo == "1":
            algorithme = "FF"
        else:
            algorithme = "PR"

    else:
        print(
            f"Veuillez choisir l'algorithme que vous souhaitez utiliser pour examiner la proposition {x}, probleme de flot max\n\t1. Ford-Fulkerson\n\t2. Pousser-reetiqueter\n\t3. Résoudre le problème de flot minimum")
        algo = input(">> ")
        while (algo != "1" and algo != "2" and algo != "3"):
            print("Saisi incorrect, saisissez 1, 2 ou 3")
            algo = input(">> ")
        if (algo == "1"):
            algorithme = "FF"
        elif (algo == "2"):
            algorithme = "PR"

    fichier = "./Propositions/prop-" + x + ".txt"
    fichier_to_write = "trace/E1-trace" + x + "-" + algorithme + ".txt"
    print("Ecriture dans", fichier_to_write)
    with open(fichier_to_write, "w") as logfile:
        sys.stdout = Tee(sys.__stdout__, logfile)

        # Extraction de la matrice
        n, capacites = lire_matrice_capacite(fichier)

        # Affichage de la table des capacités
        print("\nNombre de sommets : " + str(n))
        afficher_matrice(capacites)

        print("Le graphe residuel initial est le graphe de départ.")

        # Si problème de flot max :
        if algorithme == "FF":
            edmonds_karp(n, capacites)
        elif algorithme == "PR":
            pousser_reetiqueter(capacites, n)

        # Si problème de flot min :
        else:
            n, capacites, couts = lire_matrice_capacite_et_cout(fichier)
            print("Veuillez choisir la valeur de flot que vous souhaitez envoyer \n>> ", end=" ")
            valeur_flot = input("")
            print(f"\nL'objectif est de trouver un flot de valeur {valeur_flot}, de coût minimal. ")
            flot_total, cout_total = flot_a_cout_minimal(couts, capacites, int(valeur_flot))

        # Fin de l'écriture dans un txt
        sys.stdout = sys.__stdout__

    print("\nVoulez-vous tester un autre problème de flot (oui/non) ? ")
    continuer = input(">> ")
    while continuer not in ["oui", "non"]:
        print("\nSaisi incorrect ! Choisissez oui ou non ")
        continuer = input(">> ")
    if continuer == "oui":
        analyse_flot()
    elif continuer == "non":
        print("Retour au menu\n")


def menu():
    run = True
    while run:  # Menu principal
        print("Sélectionnez une option :")
        print("1. Faire une analyse de flot")
        print("2. Faire une analyse de complexité")
        print("3. Afficher des complexités")
        print("4. Comparer la complexité entre deux algorithmes")
        print("5. Quitter")

        choix = input(">> ")

        if choix == "1":
            analyse_flot()
        elif choix == "2":
            analyse_complexite()
        elif choix == "3":
            affichage_complexite()
        elif choix == "4":
            compare_complexite("./temps_execution/temps_execution_FF.csv", "./temps_execution/temps_execution_PR.csv")
        elif choix == "5":
            print("Exit!")
            run = False
            effacer_csv()
        else:
            print("Réponse incorrecte. Veuillez choisir 1, 2, 3 ou 4.")


if __name__ == '__main__':
    menu()