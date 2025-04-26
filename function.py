from collections import deque
import pandas as pd
from networkx.algorithms.distance_measures import eccentricity


def lire_matrice_capacite(fichier):
    """
    :param fichier:
    :return une liste 2 dimension faisant office de matrice de capacité:
    """
    with open(fichier, 'r') as f:
        lignes = f.readlines()
    n = int(lignes[0].strip()) # nombre de sommets
    matrice = [list(map(int, ligne.strip().split())) for ligne in lignes[1:n+1]]
    return n, matrice

def lire_matrice_capacite_et_cout(fichier):
    """
    :param fichier:
    :return:
        - n : nombre de sommets
        - capacites : matrice de capacités
        - couts : matrice de coûts
    """
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    n = int(lignes[0].strip())  # nombre de sommets
    lignes = lignes[1:]

    capacites = [list(map(int, lignes[i].strip().split())) for i in range(n)]
    couts = [list(map(int, lignes[i + n].strip().split())) for i in range(n)]

    return n, capacites, couts


def generer_etiquettes(n):
    """
    :param n:
    Soit n le nombre de sommet dans notre graphe. Ce nombre nous sert à nommer
    les sommets en leur attribuant des étiquettes allant de chr(96)=a à chr(96+n-1). s et t etant
    les sommets source et terminaison.
    """
    if n < 3:
        return ['s', 't'][:n]
    return ['s'] + [chr(96 + i) for i in range(1, n - 1)] + ['t']


def afficher_matrice(matrice, titre="Matrice"):
    """
    :param matrice:
    :param titre:
    :return:
    Utilisation de dataframe en Panda pour afficher de manière élegante une matrice passé en paramètre
    ainsi que son titre. On retourne aussi le dataframe pour des usages complélmentaire.
    """
    etiquettes = generer_etiquettes(len(matrice))
    df = pd.DataFrame(matrice, columns=etiquettes, index=etiquettes)
    print(f"{titre} :\n{df}\n")
    return df


def bfs(capacites, flots, source, puits, parent):
    """
    :param capacites:
    :param flots:
    :param source:
    :param puits:
    :param parent:
    Parcours en largeur plus tard utilisé dans l'algorithme d'Elmond Krap.
    :return:
    """
    n = len(capacites)
    visite = [False] * n # On initialise au début tout les sommets comme non parcouru
    file = deque([source]) # On commence par le sommet source, soit "s" dans notre cas
    visite[source] = True
    while file: # Tant que la file est pleine on continue à visiter
        u = file.popleft() # On retire le sommet courant u du début de la file pour l'explorer
        for v in range(n):
            if not visite[v] and capacites[u][v] - flots[u][v] > 0: # On verifie que le sommet v n’a pas encore été visité et qu'on peut encore envoyer du flot
                parent[v] = u # On enregistre que v a été atteint à partir de u
                visite[v] = True
                file.append(v)
                if v == puits:
                    return True
    return False


def chaine_augmentante(parent, source, puits):
    chemin = []
    v = puits
    while v != source:
        u = parent[v]
        chemin.append((u, v))
        v = u
    chemin.reverse()
    return chemin


def appliquer_flot(chemin, capacites, flots):
    flot = min(capacites[u][v] - flots[u][v] for u, v in chemin)
    for u, v in chemin:
        flots[u][v] += flot
        flots[v][u] -= flot
    return flot


def matrice_residuelle(capacites, flots):
    n = len(capacites)
    return [[capacites[u][v] - flots[u][v] for v in range(n)] for u in range(n)]



def afficher_chaine(chemin, n):
    etiquettes = generer_etiquettes(n)
    return " → ".join(etiquettes[u] for u, _ in chemin) + f" → {etiquettes[chemin[-1][1]]}"


def edmonds_karp(n, capacites):
    source, puits = 0, n - 1
    flots = [[0]*n for _ in range(n)]
    flot_max = 0
    iteration = 1

    print("\nAffichage de la table des capacités :")
    afficher_matrice(capacites, "Matrice des capacités")

    etiquettes = generer_etiquettes(n)

    while True:
        parent = [-1] * n
        if not bfs(capacites, flots, source, puits, parent):
            break

        chemin = chaine_augmentante(parent, source, puits)
        flot = appliquer_flot(chemin, capacites, flots)
        flot_max += flot

        print(f"\n⋇ Itération {iteration} :")
        print("Le parcours en largeur :")
        for i in range(n):
            if parent[i] != -1:
                print(f"{etiquettes[i]} ; Π({etiquettes[i]}) = {etiquettes[parent[i]]}")

        print(f"\nDétection d’une chaîne améliorante : {afficher_chaine(chemin, n)} de flot {flot}.")
        afficher_matrice(matrice_residuelle(capacites, flots), "Modifications sur le graphe résiduel")

        iteration += 1

    afficher_matrice([[f"{flots[i][j]}/{capacites[i][j]}" if capacites[i][j] != 0 else "0" for j in range(n)] for i in range(n)], "Matrice des flots (finale)")
    print(f"\nValeur du flot max = {flot_max}\n")
    return flot_max


def resoudre_probleme(fichier_txt):
    n, capacites = lire_matrice_capacite(fichier_txt)
    return edmonds_karp(n, capacites)





def initialisation_hauteur_et_excedent(n):
    hauteurs = {}
    excedents = {}
    etiquettes = generer_etiquettes(n)
    for i in range(n-1):
        hauteurs[etiquettes[i]] = 0
        excedents[etiquettes[i]] = 0
    hauteurs['s'] = n
    excedents['s'] = 0
    hauteurs['t'] = 0
    excedents['t'] = 0


    return hauteurs, excedents

def initialiser_flots_excedents_source(n,capacites):
    hauteurs, excedents = initialisation_hauteur_et_excedent(n)
    etiquettes = generer_etiquettes(n)
    print()
    flots = [[0] * n for _ in range(n)]
    for i in range(n):
        if ( capacites[0][i] != 0):
            flots[0][i] = capacites[0][i]
            excedents[etiquettes[i]] = capacites[0][i]
            excedents['s'] = excedents['s'] - capacites[0][i]

    return flots, hauteurs, excedents


def pousser(u, v, excedents, hauteurs, capacites, flots):
    etiquette_u = generer_etiquettes(len(capacites))[u]
    etiquette_v = generer_etiquettes(len(capacites))[v]
    # Calcul des capacités résiduelles via matrice résiduelle
    residuels = matrice_residuelle(capacites, flots)

    cf_direct = residuels[u][v] # Capacité directe résiduelle
    cf_inverse = flots[v][u] # Capacité inverse = flot existant inverse

    pushed = False

    # Vérification de la condition de poussée pour les arcs directs
    if cf_direct > 0 and hauteurs[etiquette_u] == hauteurs[etiquette_v] + 1: #cf >0 on verifie que l'arc u-> existe
        quantite = min(excedents[etiquette_u], cf_direct)
        flots[u][v] += quantite
        excedents[etiquette_u] -= quantite
        excedents[etiquette_v] += quantite
        pushed = True

    # Vérification de la condition de poussée pour les arcs inverses
    elif cf_inverse > 0 and hauteurs[etiquette_u] == hauteurs[etiquette_v] + 1:
        quantite = min(excedents[etiquette_u], cf_inverse)
        flots[v][u] -= quantite
        excedents[etiquette_u] -= quantite
        excedents[etiquette_v] += quantite
        pushed = True

    return pushed


def pousser_reetiqueter(capacites, n):
    flots, hauteurs, excedents = initialiser_flots_excedents_source(n, capacites)
    etiquettes = generer_etiquettes(n)
    afficher_matrice(capacites)

    afficher_matrice(flots)

    while True:
        u = sommet_actif(hauteurs, etiquettes, excedents) # Sélection du sommet actif
        if u is None:
            break

        indice_u, etiquette_u = u[2], u[1]
        pushed = False

        # Parcourir tous les voisins possibles (directs et inverses)
        for v in range(n):
            if pousser(indice_u, v, excedents, hauteurs, capacites, flots):
                pushed = True
                break

        if not pushed:
            # Réétiqueter et réinitialiser la boucle
            reetiqueter(indice_u, excedents, hauteurs, capacites, flots)


    return excedents['t']


"""def voisins_par_sommet(matrice_capacite, etiquettes):
    n = len(matrice_capacite)
    voisins = {etiquette: [] for etiquette in etiquettes}

    for i in range(n):
        for j in range(n):
            # Ajouter les arcs directs
            if matrice_capacite[i][j] > 0:
                voisins[etiquettes[i]].append(j)
            # Ajouter les arcs inverses s'ils ont un flot > 0
            if matrice_capacite[j][i] > 0:
                voisins[etiquettes[i]].append(j)

    return voisins"""


def reetiqueter(u, excedents, hauteurs, capacites, flots):
    etiquette_u = generer_etiquettes(len(capacites))[u]
    min_hauteur = float('inf')
    residuels = matrice_residuelle(capacites, flots)

    # Parcourir tous les sommets
    for v in range(len(capacites)):
        if v == u:
            continue
        # Vérifier les arcs dans le graphe résiduel
        if residuels[u][v] > 0 or flots[v][u] > 0:
            min_hauteur = min(min_hauteur, hauteurs[generer_etiquettes(len(capacites))[v]])

    hauteurs[etiquette_u] = min_hauteur + 1


def sommet_actif(hauteurs,etiquettes,excedents):
    hauteurs = dict(list(hauteurs.items())[1:-1])
    excedents = dict(list(excedents.items())[1:-1])
    etiquettes = etiquettes[1:-1]

    sommets =[(hauteurs[etiquettes[i]],etiquettes[i],i+1) for i in range(len(etiquettes)) if excedents[etiquettes[i]]>0]

    if not sommets:
        return None
    sommets.sort(key=lambda sommet: (-sommet[0],sommet[1]))

    return sommets[0]


def cycles_de_poids_negatif(couts, distances):
    n = len(couts)
    for u in range(n):
        for v in range(n):
            if couts[u][v] != 0 and distances[u] + couts[u][v] < distances[v]:
                return False
    return True

def bellman_ford_avec_predecesseurs(couts, source=0):
    n = len(couts)
    distances = [float('inf')] * n
    predecesseurs = [None] * n
    distances[source] = 0

    for x in range(n - 1):
        for u in range(n):
            for v in range(n):
                if couts[u][v] != 0 and distances[u] + couts[u][v] < distances[v]:
                    distances[v] = distances[u] + couts[u][v]
                    predecesseurs[v] = u

    if not cycles_de_poids_negatif(couts, distances):
        print("Le graphe contient un cycle de poids négatif")
        return None, None

    return distances, predecesseurs

def reconstruire_chemin(predecesseurs, t):
    chemin = []
    courant = t
    while courant is not None:
        chemin.insert(0, courant)
        courant = predecesseurs[courant]
    print(chemin)
    return chemin

def afficher_chemin_cout_et_capacite(chemin, couts, capacites):
    etiquettes = generer_etiquettes(len(couts))
    cout_total = 0
    capacites_sur_chemin = []

    print("Chemin le plus court (en coût) de s à t :")
    for i in range(len(chemin) - 1):
        u = chemin[i]
        v = chemin[i + 1]
        cout_total += couts[u][v]
        capacites_sur_chemin.append(capacites[u][v])
        print(f"{etiquettes[u]} -> {etiquettes[v]} (coût: {couts[u][v]}, capacité: {capacites[u][v]})")

    min_capacite = min(capacites_sur_chemin)
    print(f"Coût total du chemin : {cout_total}")
    print(f"Flot maximal : {min_capacite}")



