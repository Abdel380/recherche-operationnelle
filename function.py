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
    cf = capacites[u][v] - flots[u][v]  # capacité résiduelle
    print(cf)
    pushed = False
    print("POUSSER")
    print(capacites[u][v])
    print(f"Hauteur de {etiquette_u} = {hauteurs[etiquette_u]}")
    print(f"Excédent de {etiquette_u} = {excedents[etiquette_u]}")

    if excedents[etiquette_u] >= 0 and cf >= 0 and hauteurs[etiquette_u] == hauteurs[etiquette_v]+1:
        quantite_poussee = min(excedents[etiquette_u], cf)
        print("quantite poussée = ",quantite_poussee)
        flots[u][v] += quantite_poussee
        excedents[etiquette_u] -= quantite_poussee
        print("nouvel excedent de ",etiquette_u," = ",excedents[etiquette_u])
        excedents[etiquette_v] += quantite_poussee
        print("nouvel excedent de ",etiquette_v," = ",excedents[etiquette_v])
        pushed = True
    return pushed

def reetiqueter(u, excedents, hauteurs, capacites, flots):
    """
    Réétiquette un sommet u selon l'algorithme de pousser-réétiqueter.

    :param u: indice du sommet à réétiqueter
    :param excedents: dictionnaire des excédents de chaque sommet
    :param hauteurs: dictionnaire des hauteurs de chaque sommet
    :param capacites: matrice des capacités
    :param flots: matrice des flots
    """
    n = len(capacites)
    etiquettes = generer_etiquettes(n)
    etiquette_u = etiquettes[u]

    # Vérifier si le sommet a un excédent positif
    if excedents[etiquette_u] <= 0:
        return

    # Vérifier si pour tous les voisins v dans le graphe résiduel, h[u] < h[v] + 1
    # Si c'est le cas, on doit réétiqueter
    besoin_reetiquetage = True
    min_hauteur_voisin = float('inf')

    for v in range(n):
        if v != u:
            # Vérifier si (u,v) est dans Ef (graphe résiduel)
            cf = capacites[u][v] - flots[u][v]
            if cf > 0:  # Arc (u,v) dans le graphe résiduel
                if hauteurs[etiquette_u] >= hauteurs[etiquettes[v]] + 1:
                    besoin_reetiquetage = False
                    break
                min_hauteur_voisin = min(min_hauteur_voisin, hauteurs[etiquettes[v]])

    # Réétiqueter si nécessaire
    if besoin_reetiquetage:
        hauteurs[etiquette_u] = 1 + min_hauteur_voisin


def sommet_actif(hauteurs,etiquettes,excedents):
    hauteurs = dict(list(hauteurs.items())[1:-1])
    excedents = dict(list(excedents.items())[1:-1])
    etiquettes = etiquettes[1:-1]

    sommets =[(hauteurs[etiquettes[i]],etiquettes[i],i+1) for i in range(len(etiquettes)) if excedents[etiquettes[i]]>0]

    if not sommets:
        return None
    sommets.sort(key=lambda sommet: (-sommet[0],sommet[1]))

    return sommets[0]


def pousser_reetiqueter(capacites,n):
    flots,hauteurs,excedents = initialiser_flots_excedents_source(n,capacites)
    etiquettes = generer_etiquettes(n)

    print(hauteurs)
    while True:
        u = sommet_actif(hauteurs,etiquettes,excedents)
        # Indice et étiquette du sommet actif
        indice_u, etiquette_u = u[2], u[1]

        if u is None:
            break

        pushed = False
        voisins_u = voisins_par_sommet(capacites,etiquettes)[u[1]]
        print("u",u)
        print("voisins de u",voisins_u)
        print("hauteurs",hauteurs)
        print("pousser",pushed)


        for v in voisins_u:
            cf = capacites[indice_u][v] - flots[indice_u][v]
            print("cf",cf)
            if cf>0 and n-1 in voisins_u and v==n-1:
                    temp = voisins_u[v.index()]
                    voisins_u[v.index()] = voisins_u[0]
                    voisins_u[0] = temp
            else:
                voisins_u.sort()

            if cf > 0 and hauteurs[etiquette_u] == hauteurs[chr(97+v)] + 1 and (v!=0 or v!=n-1):
                pousser(indice_u,v, excedents, hauteurs, capacites, flots)
                pushed = True
                break

            elif cf > 0 and hauteurs[etiquette_u] == hauteurs['s'] + 1:
                pousser(indice_u,v, excedents, hauteurs, capacites, flots)
                pushed = True
                break

            elif cf > 0 and hauteurs[etiquette_u] == hauteurs['t'] + 1:
                pousser(indice_u,v, excedents, hauteurs, capacites, flots)
                pushed = True
                break
            if not pushed:
                reetiqueter(indice_u, excedents, hauteurs, capacites, flots)

    return excedents['t']


def voisins_par_sommet(matrice_capacite,etiquettes):
    n = len(matrice_capacite)

    voisins = {}
    for i in range(n):
        voisins[etiquettes[i]] = []

    for i in range(n):
        for j in range(n):
            if matrice_capacite[i][j] > 0:
                # i → j : i a j comme successeur, j a i comme prédécesseur
                voisins[etiquettes[i]].append(j)
                voisins[etiquettes[j]].append(i)
                voisins[etiquettes[j]].sort()


    return voisins






