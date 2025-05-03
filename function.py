from collections import deque
import pandas as pd


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
        if chr(96 + i + k) == 's': # Eviter la redondance de l'etiquette 's' et 't'
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
                print(f"{etiquettes[i]} ; Predecesseur({etiquettes[i]}) = {etiquettes[parent[i]]}")

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

def initialiser_flots_excedents_source(n, capacites):
    hauteurs, excedents = initialisation_hauteur_et_excedent(n)
    etiquettes = generer_etiquettes(n)
    flots = [[0] * n for _ in range(n)]

    print("=== Initialisation ===")
    print("Hauteurs initiales :", hauteurs)
    print("Excédents initiaux :", excedents)
    print("Capacités   :", capacites)
    print()

    # Saturer tous les arcs sortants de la source s = 0
    for i in range(n):
        if capacites[0][i] != 0:
            flots[0][i] = capacites[0][i]
            excedents[etiquettes[i]] += capacites[0][i]
            excedents['s'] -= capacites[0][i]
            print(f"Push initial {capacites[0][i]} de s-> {etiquettes[i]}")

    print("Flots après initialisation :", flots)
    print("Excédents après init       :", excedents)
    print("==========================\n")
    return flots, hauteurs, excedents


def pousser(u, v, excedents, hauteurs, capacites, flots):
    # Génération ponctuelle des labels
    etiquette_u = generer_etiquettes(len(capacites))[u]
    etiquette_v = generer_etiquettes(len(capacites))[v]
    residuels = matrice_residuelle(capacites, flots)

    cf_direct = residuels[u][v]
    cf_inverse = flots[v][u]
    pushed = False

    print(f"  -> Tentative push {etiquette_u}->{etiquette_v} | h[{etiquette_u}]={hauteurs[etiquette_u]}, "
          f"exc[{etiquette_u}]={excedents[etiquette_u]}")

    # Push direct ?
    if cf_direct > 0 and hauteurs[etiquette_u] == hauteurs[etiquette_v] + 1:
        quantite = min(excedents[etiquette_u], cf_direct)
        flots[u][v] += quantite
        excedents[etiquette_u] -= quantite
        excedents[etiquette_v] += quantite
        pushed = True
        print(f"    -> Push direct de {quantite} (cf_direct={cf_direct})")
    # Sinon push inverse ?
    elif cf_inverse > 0 and hauteurs[etiquette_u] == hauteurs[etiquette_v] + 1:
        quantite = min(excedents[etiquette_u], cf_inverse)
        flots[v][u] -= quantite
        excedents[etiquette_u] -= quantite
        excedents[etiquette_v] += quantite
        pushed = True
        print(f"    -> Push inverse de {quantite} (cf_inverse={cf_inverse})")
    else:
        print("    -> Pas de push possible sur cet arc")

    if pushed:
        print(f"    État après push :")
        print(f"      flots[{etiquette_u}][{etiquette_v}] = {flots[u][v]}")
        print(f"      exc[{etiquette_u}] = {excedents[etiquette_u]}, exc[{etiquette_v}] = {excedents[etiquette_v]}")
    print()
    return pushed


def reetiqueter(u, hauteurs, capacites, flots):
    etiquette_u = generer_etiquettes(len(capacites))[u]
    residuels = matrice_residuelle(capacites, flots)
    min_hauteur = float('inf')

    for v in range(len(capacites)):
        if v == u:
            continue
        if residuels[u][v] > 0 or flots[v][u] > 0:
            etiquette_v = generer_etiquettes(len(capacites))[v]
            min_hauteur = min(min_hauteur, hauteurs[etiquette_v])

    ancienne = hauteurs[etiquette_u]
    hauteurs[etiquette_u] = min_hauteur + 1
    print(f"  <- Relabel {etiquette_u} : hauteur {ancienne} -> {hauteurs[etiquette_u]}\n")


def sommet_actif(hauteurs, etiquettes, excedents):
    # On ignore s et t
    h = dict(list(hauteurs.items())[1:-1])
    e = dict(list(excedents.items())[1:-1])
    labels = etiquettes[1:-1]

    sommets = []
    for i, lab in enumerate(labels, start=1):
        if e[lab] > 0:
            sommets.append((h[lab], lab, i))

    if not sommets:
        return None
    sommets.sort(key=lambda x: (-x[0], x[1]))  # plus grande hauteur, puis label
    return sommets[0]  # (hauteur, etiquette, index)


def pousser_reetiqueter(capacites, n):
    flots, hauteurs, excedents = initialiser_flots_excedents_source(n, capacites)
    etiquettes = generer_etiquettes(n)

    print("=== Début Push–Relabel ===\n")
    it = 0
    while True:
        it += 1
        print(f"--- Itération {it} ---")
        print("Hauteurs :", hauteurs)
        print("Excédents:", excedents)
        print("Flots     :", flots, "\n")

        actif = sommet_actif(hauteurs, etiquettes, excedents)
        if actif is None:
            print("Plus de sommet actif -> on arrête\n")
            break

        _, etiquette_u, u = actif
        print(f"Sommet actif : {etiquette_u} (index {u}), exc={excedents[etiquette_u]}, h={hauteurs[etiquette_u]}\n")

        pushed = False
        # on tente tous les voisins
        for v in range(n):
            if pousser(u, v, excedents, hauteurs, capacites, flots):
                pushed = True
                break

        if not pushed:
            reetiqueter(u, hauteurs, capacites, flots)

    print("=== Fin Push–Relabel ===")
    print("Flux maximum trouvé (excédent en t) =", excedents['t'])
    return excedents['t']



def cycles_de_poids_negatif(couts, distances):
    n = len(couts)
    for u in range(n):
        for v in range(n):
            if couts[u][v] != 0 and distances[u] + couts[u][v] < distances[v]:
                return False
    return True

def afficher_matrice_plus_court_chemin(matrice):
    print("\n")
    titre = "Algorithme de Bellman"
    etiquettes = generer_etiquettes(len(matrice[0]))
    iteration = [ i for i in range(len(matrice)) ]
    df = pd.DataFrame(matrice, columns=etiquettes, index=iteration)
    print(f"{titre} :\n{df}\n")
    return

def eviter_redondance(matrice):
    matrice2 = [matrice[0]]
    for elt in matrice:
        if elt not in matrice2:
            matrice2.append(elt)
    return matrice2


def bellman_ford_avec_predecesseurs(couts,capacites, source=0):
    n = len(couts)
    distances = [float('inf')] * n
    predecesseurs = [None] * n
    distances[source] = 0

    # Liste pour stocker la matrice des distances à chaque étape
    matrice_bellman = [distances.copy()]


    for u in range(n):
        for v in range(n):
            if capacites[u][v] != 0 and distances[u] + couts[u][v] < distances[v]:
                distances[v] = distances[u] + couts[u][v]
                predecesseurs[v] = u
        # Enregistrer les distances après chaque itération
        matrice_bellman.append(distances.copy())
    matrice_bellman = eviter_redondance(matrice_bellman)
    afficher_matrice_plus_court_chemin(matrice_bellman)
    return distances, predecesseurs


def maj_bellman(chemin, couts, capacites, retire):
    for x in range(len(chemin)-1):
        capacites[chemin[x]][chemin[x+1]] -= retire # OK
        capacites[chemin[x+1]][chemin[x]] = retire # OK
        couts[chemin[x+1]][chemin[x]] = 0 - couts[chemin[x]][chemin[x+1]]
        if(capacites[chemin[x]][chemin[x+1]] == 0):
            couts[chemin[x]][chemin[x + 1]] = 0

    print("\nLe graphe residuel pondere associe a cette modification est :")
    afficher_matrice(capacites, "Matrice de capacite")
    afficher_matrice(couts, "Matrice des couts")
    return couts, capacites



def reconstruire_chemin(predecesseurs, t):
    chemin = []
    courant = t
    while courant is not None:
        chemin.insert(0, courant)
        courant = predecesseurs[courant]
    return chemin

def afficher_chemin_cout_et_capacite(chemin, couts, capacites):
    etiquettes = generer_etiquettes(len(couts))
    capacites_sur_chemin = []
    etiquette_chemin = []

    print("\nChemin le plus court (en cout) de s vers t :")
    for i in range(len(chemin) - 1):
        u = chemin[i]
        v = chemin[i + 1]
        capacites_sur_chemin.append(capacites[u][v])
        print(f"{etiquettes[u]} -> {etiquettes[v]} (cout: {couts[u][v]}, capacite: {capacites[u][v]})")
        etiquette_chemin.append(etiquettes[u])
    etiquette_chemin.append("t")
    min_capacite = min(capacites_sur_chemin)

    delimiter = " -> "  # Definir le delimiter
    join_chemin = delimiter.join(etiquette_chemin)
    print(f"La premiere chaine ameliorante est donc {join_chemin} de flot {min_capacite}")
    return min_capacite, chemin




def flot_a_cout_minimal(couts, capacites, flot_demande,source=0):
    """
    :param capacites:
    :param source:
    :param flot_demande
    :param couts:
    Resoud le problème de flot a cout minimal en renvoyant le cout du flot et le chemin
    :return:
    """
    puit = len(couts) - 1 # Sommet final / noeud de destination
    flot_total = 0
    cout_total = 0
    cout_minimal = 0
    equation = "d(f) = "

    while flot_total < flot_demande:
        distances, predecesseurs = bellman_ford_avec_predecesseurs(couts, capacites, source)
        if distances[puit] == float('inf'):
            break  # Plus de chemin ameliorant

        chemin = reconstruire_chemin(predecesseurs, puit)
        min_capacite, chemin_changer = afficher_chemin_cout_et_capacite(chemin, couts, capacites)
        flot_total += min_capacite



        if(flot_total < flot_demande):
            print(f"Le flot total est {flot_total} < {flot_demande} donc on contiue.")
            # Calcule du cout du flot minimal
            for i in range(len(chemin_changer) - 1):
                u = chemin_changer[i]
                v = chemin_changer[i + 1]
                equation = equation + f" {couts[u][v]} x {min_capacite} +"
                cout_minimal += couts[u][v] * min_capacite
            couts, capacites = maj_bellman(chemin_changer, couts, capacites, min_capacite)

        else:
            print(f"\n\nLe flot total est {flot_total} > {flot_demande} donc on peut arreter ici.")
            if not(flot_total == flot_demande):
                print(f"La chaine ameliorante fait passer un flot de {min_capacite}, mais on ne lancera passer que {flot_demande - flot_total + min_capacite} ")
                min_capacite = flot_demande - flot_total + min_capacite
                # Calcule du cout du flot minimal
            for i in range(len(chemin_changer) - 1):
                u = chemin_changer[i]
                v = chemin_changer[i + 1]
                equation = equation + f" {couts[u][v]} x {min_capacite} +"
                cout_minimal += couts[u][v] * min_capacite

    if(flot_total < flot_demande):
        print(f"Il n'est pas possible d'envoyer un flot de {flot_demande}. Au maximum on envoie {flot_total}")
    else:
        print(f"Le cout pour lancer passer un flot de {flot_demande} est de : {cout_minimal}")
        print(f"{equation[:len(equation) - 1]} = {cout_minimal}")

    return flot_total, cout_total


