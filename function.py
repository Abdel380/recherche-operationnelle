from collections import deque
import pandas as pd
from networkx.algorithms.distance_measures import eccentricity


def lire_matrice_capacite(fichier):
    """
    :param fichier:
    :return une liste 2 dimension faisant office de matrice de capacite:
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
        - capacites : matrice de capacites
        - couts : matrice de couts
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
    Soit n le nombre de sommet dans notre graphe. Ce nombre nous sert a nommer
    les sommets en leur attribuant des etiquettes allant de chr(96)=a a chr(96+n-1). s et t etant
    les sommets source et terminaison.
    """
    if n < 3:
        return ['s', 't'][:n]
    k = 0
    etiquette = []
    for i in range(1, n - 1):
        if (chr(96 + i + k) == 's'): # Eviter la redondance de l'etiquette 's' et 't'
            k+=2
        etiquette.append(chr(96 + i + k))
    return ['s'] + etiquette + ['t']


def afficher_matrice(matrice, titre="Matrice"):
    """
    :param matrice:
    :param titre:
    :return:
    Utilisation de dataframe en Panda pour afficher de manière elegante une matrice passe en paramètre
    ainsi que son titre. On retourne aussi le dataframe pour des usages complelmentaire.
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
    Parcours en largeur plus tard utilise dans l'algorithme d'Elmond Krap.
    :return:
    """
    n = len(capacites)
    visite = [False] * n # On initialise au debut tout les sommets comme non parcouru
    file = deque([source]) # On commence par le sommet source, soit "s" dans notre cas
    visite[source] = True
    while file: # Tant que la file est pleine on continue a visiter
        u = file.popleft() # On retire le sommet courant u du debut de la file pour l'explorer
        for v in range(n):
            if not visite[v] and capacites[u][v] - flots[u][v] > 0: # On verifie que le sommet v n’a pas encore ete visite et qu'on peut encore envoyer du flot
                parent[v] = u # On enregistre que v a ete atteint a partir de u
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
    return " -> ".join(etiquettes[u] for u, _ in chemin) + f" -> {etiquettes[chemin[-1][1]]}"


def edmonds_karp(n, capacites):
    source, puits = 0, n - 1
    flots = [[0]*n for _ in range(n)]
    flot_max = 0
    iteration = 1

    etiquettes = generer_etiquettes(n)

    while True:
        parent = [-1] * n
        if not bfs(capacites, flots, source, puits, parent):
            break

        chemin = chaine_augmentante(parent, source, puits)
        flot = appliquer_flot(chemin, capacites, flots)
        flot_max += flot

        print(f"\nIteration {iteration} :")
        print("Le parcours en largeur :")
        for i in range(n):
            if parent[i] != -1:
                print(f"{etiquettes[i]} ; ({etiquettes[i]}) = {etiquettes[parent[i]]}")

        print(f"\nDetection d une chaine ameliorante : {afficher_chaine(chemin, n)} de flot {flot}.")
        afficher_matrice(matrice_residuelle(capacites, flots), "Modifications sur le graphe residuel")

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
    # Calcul des capacites residuelles via matrice residuelle
    residuels = matrice_residuelle(capacites, flots)

    cf_direct = residuels[u][v] # Capacite directe residuelle
    cf_inverse = flots[v][u] # Capacite inverse = flot existant inverse

    pushed = False

    # Verification de la condition de poussee pour les arcs directs
    if cf_direct > 0 and hauteurs[etiquette_u] == hauteurs[etiquette_v] + 1: #cf >0 on verifie que l'arc u-> existe
        quantite = min(excedents[etiquette_u], cf_direct)
        flots[u][v] += quantite
        excedents[etiquette_u] -= quantite
        excedents[etiquette_v] += quantite
        pushed = True

    # Verification de la condition de poussee pour les arcs inverses
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


    while True:
        u = sommet_actif(hauteurs, etiquettes, excedents) # Selection du sommet actif
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
            # Reetiqueter et reinitialiser la boucle
            reetiqueter(indice_u, excedents, hauteurs, capacites, flots)

    print(excedents['t'])
    return excedents['t']


def reetiqueter(u, excedents, hauteurs, capacites, flots):
    etiquette_u = generer_etiquettes(len(capacites))[u]
    min_hauteur = float('inf')
    residuels = matrice_residuelle(capacites, flots)

    # Parcourir tous les sommets
    for v in range(len(capacites)):
        if v == u:
            continue
        # Verifier les arcs dans le graphe residuel
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

def bellman_ford_avec_predecesseurs(couts,capacites, source=0):
    n = len(couts)
    distances = [float('inf')] * n
    predecesseurs = [None] * n
    distances[source] = 0

    for x in range(n - 1):
        for u in range(n):
            for v in range(n):
                if capacites[u][v] != 0 and distances[u] + couts[u][v] < distances[v]:
                    distances[v] = distances[u] + couts[u][v]
                    predecesseurs[v] = u
    print(distances, predecesseurs)
    return distances, predecesseurs


def maj_bellman(chemin, couts, capacites, min_capacite):
    for x in range(len(chemin)-1):
        capacites[chemin[x]][chemin[x+1]] -= min_capacite # OK
        capacites[chemin[x+1]][chemin[x]] = min_capacite # OK
        couts[chemin[x+1]][chemin[x]] = - couts[chemin[x]][chemin[x+1]]

    couts[chemin[-2]][chemin[-1]] = 0


def reconstruire_chemin(predecesseurs, t):
    chemin = []
    courant = t
    while courant is not None:
        chemin.insert(0, courant)
        courant = predecesseurs[courant]
    return chemin

def afficher_chemin_cout_et_capacite(chemin, couts, capacites):
    etiquettes = generer_etiquettes(len(couts))
    cout_total = 0
    capacites_sur_chemin = []

    print("\nChemin le plus court (en cout) de s a t :")
    for i in range(len(chemin) - 1):
        u = chemin[i]
        v = chemin[i + 1]
        cout_total += couts[u][v]
        capacites_sur_chemin.append(capacites[u][v])
        print(f"{etiquettes[u]} -> {etiquettes[v]} (cout: {couts[u][v]}, capacite: {capacites[u][v]})")

    min_capacite = min(capacites_sur_chemin)
    maj_bellman(chemin, couts, capacites, min_capacite)




def flot_a_cout_minimal(couts, capacites, flot_demande,source=0):
    """
    :param capacites:
    :param source:
    :param couts:
    Resoud le problème de flot a cout minimal en renvoyant le cout du flot et le chemin
    :return:
    """
    puit = len(couts) - 1 # Sommet final / noeud de destination
    flot_total = 0
    cout_total = 0

    while flot_total < flot_demande:
        distances, predecesseurs = bellman_ford_avec_predecesseurs(couts,capacites, source)
        if distances[puit] == float('inf'):
            break  # Plus de chemin ameliorant

        chemin = reconstruire_chemin(predecesseurs, puit)
        capacites_sur_chemin = [capacites[chemin[i]][chemin[i + 1]] for i in range(len(chemin) - 1)]
        min_capacite = min(capacites_sur_chemin)

        # Limiter a ce qu’il reste a envoyer
        flot_rest = flot_demande - flot_total
        flux_envoye = min(min_capacite, flot_rest)

        maj_bellman(chemin, couts, capacites, flux_envoye)

        flot_total += flux_envoye
        cout_total += distances[puit] * flux_envoye

        afficher_chemin_cout_et_capacite(chemin, couts, capacites)
        print(f"\n>> Flot achemine : {flot_total} / {flot_demande}")
        print(f">> Cout total minimum : {cout_total}")


    return flot_total, cout_total


