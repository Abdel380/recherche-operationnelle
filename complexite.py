import csv
import math
import time
import matplotlib.pyplot as plt
from menu import fichier_valide
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


import os
import csv

def nuage_de_points(n):
    matrice_temps = [[],[],[]]

    for i in range(1, 101):
        temps_fin_FF, temps_fin_PR, temps_fin_FM = temps_execution(n)
        matrice_temps[0].append((n, i, temps_fin_FF))
        matrice_temps[1].append((n, i, temps_fin_PR))
        matrice_temps[2].append((n, i, temps_fin_FM))

    if not os.path.exists("./temps_execution/temps_execution_FF.csv") or os.stat("./temps_execution/temps_execution_FF.csv").st_size == 0:
        with open("./temps_execution/temps_execution_FF.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["n", "iteration", "temps_execution"])

    with open("./temps_execution/temps_execution_FF.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(matrice_temps[0])

    if not os.path.exists("./temps_execution/temps_execution_PR.csv") or os.stat("./temps_execution/temps_execution_PR.csv").st_size == 0:
        with open("./temps_execution/temps_execution_PR.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["n", "iteration", "temps_execution"])

    with open("./temps_execution/temps_execution_PR.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(matrice_temps[1])

    if not os.path.exists("./temps_execution/temps_execution_FM.csv") or os.stat("./temps_execution/temps_execution_FM.csv").st_size == 0:
        with open("./temps_execution/temps_execution_FM.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["n", "iteration", "temps_execution"])

    with open("./temps_execution/temps_execution_FM.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
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


def compare_complexite(csv_ff, csv_pr):
    if not fichier_valide(csv_ff):
        print(f"Le fichier {csv_ff} n'est pas valide.")
        return None, None

    if not fichier_valide(csv_pr):
        print(f"Le fichier {csv_pr} n'est pas valide.")
        return None, None

    # Lecture des fichiers CSV
    df_ff = pd.read_csv(csv_ff)
    df_pr = pd.read_csv(csv_pr)

    # Récupération des temps d'exécution
    # Pour Ford-Fulkerson
    ff_times = df_ff.groupby('n')["temps_execution"].apply(list).reset_index(name='temps_ff')
    # Pour Pousser-reetiqueter
    pr_times = df_pr.groupby('n')["temps_execution"].apply(list).reset_index(name='temps_pr')

    comparaison = pd.merge(ff_times, pr_times, on="n")

    # Traçage de tous les temps d'exécution
    plt.figure(figsize=(9, 5))
    for i in range(len(comparaison)):
        plt.plot([comparaison["n"][i]] * len(comparaison["temps_ff"][i]), comparaison["temps_ff"][i], 'bo',
                 label="Ford-Fulkerson" if i == 0 else "")
        plt.plot([comparaison["n"][i]] * len(comparaison["temps_pr"][i]), comparaison["temps_pr"][i], 'ro',
                 label="Pousser-reetiqueter" if i == 0 else "")

    plt.title("Temps d'exécution des algorithmes pour chaque n")
    plt.xlabel("Nombre de sommets n")
    plt.ylabel("Temps d'exécution (s)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Récupération des valeurs maximales
    ff_max = df_ff.groupby('n')["temps_execution"].max().reset_index(name="temps_execution_ff")
    pr_max = df_pr.groupby('n')["temps_execution"].max().reset_index(name="temps_execution_pr")

    # Fusion des résultats maximaux pour les temps d'exécution
    comparaison_max = pd.merge(ff_max, pr_max, on="n")

    # Traçage du rapport des temps maximaux entre les deux algorithmes
    comparaison_max["θFF/θPR"] = comparaison_max["temps_execution_ff"] / comparaison_max["temps_execution_pr"]

    plt.figure(figsize=(9, 5))
    plt.plot(comparaison_max["n"], comparaison_max["θFF/θPR"], color="green", label="θFF/θPR")
    plt.title("Comparaison des temps maximaux entre FF et PR")
    plt.xlabel("Nombre de sommets n")
    plt.ylabel("Rapport θFF/θPR")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Affichage des résultats dans la console
    print("Comparaison des temps d'exécution pour chaque n :")
    print(comparaison)

    print("Comparaison des rapports maximaux :")
    print(comparaison_max)

    return comparaison, comparaison_max

