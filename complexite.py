import math
import time
import matplotlib.pyplot as plt
import numpy as np

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
    pousser_reetiqueter(capacites, n)
    temps_fin_FM = time.process_time() - temps_debut_FM


    return temps_fin_FF,temps_fin_PR,temps_fin_FM


def nuage_de_points(n):
    matrice_temps = [[],[],[]]

    for i in range(100):
        temps_fin_FF,temps_fin_PR,temps_fin_FM = temps_execution(n)
        matrice_temps[0].append(temps_fin_FF)
        matrice_temps[1].append(temps_fin_PR)
        matrice_temps[2].append(temps_fin_FM)

    for i in matrice_temps:
        print(i)
    afficher_nuage_points(matrice_temps[0], "FF")
    afficher_nuage_points(matrice_temps[1], "PR")
    afficher_nuage_points(matrice_temps[2], "FM")

def afficher_nuage_points(matrice,algorithme):
    x0 = [100 for i in range(100)]



    jitter = np.random.uniform(-0.3, 0.3, size=len(matrice))  # décalage minuscule
    x = x0 + jitter
    plt.scatter(x, matrice, s=20, alpha=0.6)

    plt.scatter(x,matrice)
    plt.title("Nuage de points pour l'algorithme:"+ algorithme)
    plt.xlabel("x")
    plt.ylabel("temps d'éxécution")
    plt.grid()
    plt.show()





