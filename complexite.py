import csv
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

from function import *
import random
def generer_capacites_couts_aleatoirement(n):
    capacites = [[0] * n for _ in range(n)]
    couts = [[0] * n for _ in range(n)]

    nb_val_non_nulles = math.floor((n*n)/2)
    couples =[(i,j) for i in range(n) for j in range (n) if i!=j]
    arrete_retenue = random.sample(couples, nb_val_non_nulles)
    for sommet, succ in arrete_retenue:
        capacites[sommet][succ] += random.randint(1,100)
        couts[sommet][succ] += random.randint(1, 100)
    afficher_matrice(capacites, n)
    afficher_matrice(couts, n)
    return capacites, couts

def temps_execution(n):
    capacites,couts = generer_capacites_couts_aleatoirement(n)

    temps_debut_FF = time.process_time()
    edmonds_karp(n,capacites)
    temps_fin_FF = time.process_time() - temps_debut_FF

    temps_debut_PR = time.process_time()
    pousser_reetiqueter(capacites, n)
    temps_fin_PR = time.process_time() - temps_debut_PR

    temps_debut_FM = time.process_time()
    flot_a_cout_minimal(couts,capacites,100)
    temps_fin_FM = time.process_time() - temps_debut_FM


    return temps_fin_FF,temps_fin_PR,temps_fin_FM


def nuage_de_points(n):
    matrice_temps = [[],[],[]]

    for i in range(1,101):
        temps_fin_FF,temps_fin_PR,temps_fin_FM = temps_execution(n)
        matrice_temps[0].append((n,i,temps_fin_FF))
        matrice_temps[1].append((n,i,temps_fin_PR))
        matrice_temps[2].append((n,i,temps_fin_FM))

    with open("./temps_execution/temps_execution_FF.csv","a",newline="") as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(matrice_temps[0])
    with open("./temps_execution/temps_execution_PR.csv","a",newline="") as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(matrice_temps[1])
    with open("./temps_execution/temps_execution_FM.csv","a",newline="") as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(matrice_temps[2])

def plot_algorithm(csv_path, label):
    # 1. Préparation de deux listes vides :
    #    - ns    : contiendra les valeurs de 'n' (taille du graphe)
    #    - times : contiendra les temps d'exécution correspondants
    ns, times = [], []

    # 2. Ouverture du fichier CSV en mode lecture
    #    newline=''   : évite les lignes vides supplémentaires
    #    encoding='utf-8' : gère correctement les caractères accentués
    with open(csv_path, newline='', encoding='utf-8') as f:
        # 3. Création d'un DictReader pour accéder aux colonnes par nom
        reader = csv.DictReader(f)

        # 4. Parcours de chaque ligne (chaque exécution mesurée)
        for row in reader:
            # 4.a Conversion de la colonne 'n' en entier
            ns.append(int(row['n']))
            # 4.b Conversion du temps en flottant
            #    Attention : si votre en-tête CSV s'appelle 'execution_time',
            #    remplacez 'temps_execution' par 'execution_time' ici.
            times.append(float(row['temps_execution']))

    # 5. Création d'une nouvelle figure Matplotlib de taille 7×4 pouces
    plt.figure(figsize=(7, 4))

    # 6. Tracé du nuage de points
    #    - ns    en abscisse
    #    - times en ordonnée
    #    - s=20  : taille des points
    #    - alpha=0.6 : transparence pour mieux visualiser les surimpressions
    plt.scatter(ns, times, s=20, alpha=0.6)

    # 7. Mise en forme du graphique
    plt.title(f"Temps d'exécution de {label}")  # Titre dynamique selon l'algorithme
    plt.xlabel("Nombre de sommets n")            # Légende de l'axe X
    plt.ylabel("Temps d'exécution (s)")           # Légende de l'axe Y
    plt.grid(True)                                # Ajout d'une grille de fond

    # 8. Affichage à l'écran
    plt.show()





def lancer_experience():
    print("start")
    nombre_sommet = [10,20,40,100,400,1000,4000,10000] # Les différents tests pour le nombre de sommets

    for i in range(len(nombre_sommet)):
        name_file_FF = "experience/" + str(nombre_sommet[i]) + "/FF.txt" # Fichier txt avec les tests
        name_file_PR = "experience/" + str(nombre_sommet[i]) + "/PR.txt"
        name_file_MIN = "experience/" + str(nombre_sommet[i]) + "/MIN.txt"

        tab_FF = [] # Stockage des temps d'execution
        tab_PR = []
        tab_MIN = []

        for iteration in range(100):
            temps_fin_FF,temps_fin_PR,temps_fin_MIN = temps_execution(nombre_sommet[i]) # Les temps d'exécution pour un seul
            tab_FF.append(temps_fin_FF)
            tab_PR.append(temps_fin_PR)
            tab_MIN.append(temps_fin_MIN)
        with open(name_file_FF, 'w') as f:
            for element in tab_FF:
                f.write(str(element) + "\n")
                f.close

        with open(name_file_PR, 'w') as f:
            for element in tab_PR:
                f.write(str(element) + "\n")
                f.close

        with open(name_file_MIN, 'w') as f:
            for element in tab_MIN:
                f.write(str(element) + "\n")
                f.close
    return





if __name__ == '__main__':
    lancer_experience()

