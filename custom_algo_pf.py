import networkx as nx
import osmnx as ox

"""Fonctions communes à plusieurs algorithmes

    calc_distance : Détermine la distance entre deux sommets mis en paramètre.
    fin_algo : Récupère le dictionnaire contenant le sommet précédent de chaque
               sommet et créer une liste qui contient les sommets a emprunté
               pour avoir le plus cours chemin, puis la renvoie. Si
               la condition est vraie, elle retourne une liste vide.
"""

def calc_distance(a, b):
    return ((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2) ** 0.5


def fin_algo(sommet_precedent, cond, debut, fin):

    meilleur_chemin = []
    if cond:
        print("Il n'existe pas de chemin pour atteindre ", fin, " depuis le point ", debut)
        return []
    
    while fin != None:
        meilleur_chemin.insert(0, fin)
        fin = sommet_precedent[fin]
    # Tant que le sommet precedent de fin n'est pas null
    # On rajoute le sommet au début de la liste et fin devient son sommet précédent

    return meilleur_chemin

"""boucle_dijkstra

    Il s'agit de la partie principale des deux algorithmes qui l'utilisent,
    tant qu'il y a des sommets dans la liste sommets_non_visites, la fonction
    va réaliser l'arbre couvrant du graphe, c'est à dire, que chaque sommet
    soit relié au graphe en utilisant l'arête qui le rapproche le plus
    possible du point de départ (la racine).

    
    @parametre graphe       G 
    @parametre liste        sommets_non_visites
    @parametre dictionnaire distances 
    @parametre dictionnaire sommet_precedent
    @renvoie   liste        meilleur_chemin 
"""

def boucle_dijkstra(G, sommets_non_visites, distances, sommet_precedent, debut):  

    sommet_actuel = debut
    while sommets_non_visites: 
        voisins_sommet_actuel = nx.neighbors(G, sommet_actuel) 
        
        for j in voisins_sommet_actuel:
            if j in sommets_non_visites:
                nouvelle_dist = G.edges[(sommet_actuel, j, 0)]["length"] + distances[sommet_actuel]
                #On calcul la nouvelle distance par rapport a la racine
                if nouvelle_dist < distances[j]:
                    distances[j] = nouvelle_dist
                    sommet_precedent[j] = sommet_actuel
                #Si la distance est plus courte, on met a jour l'arête qui
                #permet d'accéder a ce sommet

        plus_petit = float('inf')
        
        for k in distances:
            if k in sommets_non_visites and k != sommet_actuel:
                if plus_petit > distances[k]:
                    plus_petit = distances[k]
                    dernier = k
        #On détermine le prochain sommet à prendre en choississant celui
        #qui a la plus petite distance avec le sommet de départ

        sommets_non_visites.remove(sommet_actuel)
        sommet_actuel = dernier
        #Mise à jour du sommet actuel
        
        if plus_petit == float('inf'): 
            sommets_non_visites.clear()
        #Si les sommets restants ne peuvent pas être lié a l'arbre couvrant
        #on vide la liste pour arrêter la boucle
    return sommet_precedent

"""custom_dijkstra

    L'algorithme de base, il initialise les listes et les dictionnaires,
    ensuite il fait appel aux fonctions boucle_dijkstra et fin_algo
    pour faire le traitement.

    
    @parametre graphe   G 
    @parametre sommet   debut
    @parametre sommet   fin 
    @renvoie   liste    meilleur_chemin 
"""

def custom_dijkstra(G, debut, fin):
 
    distances = {} 
    sommet_precedent = {} 
    sommets_non_visites = list(nx.nodes(G))
    #On récupère tous les sommets du graphe

    for i in sommets_non_visites:
        distances[i] = float('inf')
    #Par défaut, toutes les distances a la racine sont infini

    sommet_precedent[debut] = None 
    sommet_precedent[fin] = None
    distances[debut] = 0

    sommet_precedent = boucle_dijkstra(G, sommets_non_visites, distances, 
                                       sommet_precedent, debut) 

    return fin_algo(sommet_precedent, 
                    sommet_precedent[fin] == None, debut, fin)

"""opti_dijkstra

    Version optimisée de la version de base, il fait les mêmes initialisations
    que celui d'origine, à la différence, qu'il va créer un cercle centré
    sur le milieu entre le sommet de départ et celui d'arrivée, tous les 
    sommets en dehors du rayon de ce cercle seront retirés des sommets
    a visité. Ensuite il fait appel aux fonctions boucle_dijkstra et 
    fin_algo pour faire le traitement.

    
    @parametre graphe   G 
    @parametre sommet   debut
    @parametre sommet   fin 
    @renvoie   liste    meilleur_chemin 
"""

def opti_dijkstra(G, debut, fin):

    distances = {} 
    sommet_precedent = {} 

    sommets_non_visites = list(nx.nodes(G))
    #On récupère tous les sommets du graphe 
    milieu_x = (G.nodes[debut]['x'] + G.nodes[fin]['x'])/2
    milieu_y = (G.nodes[debut]['y'] + G.nodes[fin]['y'])/2
    #On détermine les coordonnées du milieu des deux sommets
    rayon = calc_distance(
        {'x': milieu_x,'y': milieu_y}, 
        G.nodes[debut]) * 1.25 # On prend une marge de 25% sur le rayon

    for j in sommets_non_visites:
        if calc_distance({'x': milieu_x,'y': milieu_y}, G.nodes[j]) > rayon:
            sommets_non_visites.remove(j)
    #On retire tous les sommets n'étant pas dans le rayon du cercle
    
    for i in sommets_non_visites:
        distances[i] = float('inf')
    #Par défaut, toutes les distances a la racine sont infini

    sommet_precedent[debut] = None 
    sommet_precedent[fin] = None 
    distances[debut] = 0


    sommet_precedent = boucle_dijkstra(G, sommets_non_visites, distances, 
                                       sommet_precedent, debut)
        
    return fin_algo(sommet_precedent, 
                    sommet_precedent[fin] == None, debut, fin)

"""custom_Astar

    Version customisée de l'algorithme A*, l'algorithme parcourt
    les sommets du graphe de manière a essayé de se rapprocher
    le plus possible à chaque itération, du sommet d'arrivée
    tout en prenant en compte le coût de l'arête.
    Lorsqu'il l'a atteint, ou qu'il détermine qu'il ne peut 
    pas l'atteindre, il appelle la fonction fin_algo.

    
    @parametre graphe   G 
    @parametre sommet   debut
    @parametre sommet   fin 
    @renvoie   liste    meilleur_chemin 
"""

def custom_Astar(G, debut, fin):

    sommet_actuel = debut
    sommet_precedent = {}
    distances = {}
    liste_ouverte = []
    sommets_marques = []

    liste_ouverte.append(sommet_actuel)
    sommet_precedent[sommet_actuel] = None
    distances[sommet_actuel] = calc_distance(G.nodes[sommet_actuel], 
                                             G.nodes[fin])
    #Initialisation
    booleen = True

    while booleen:
        voisins_sommet_actuel = list(nx.neighbors(G, sommet_actuel))
        for i in voisins_sommet_actuel:
            if i == fin:
                sommet_precedent[fin] = sommet_actuel
                booleen = False
                continue
            #Si l'un des voisins et le sommet d'arrivée,
            #on le note et on quitte la boucle
            elif i not in sommets_marques and i not in liste_ouverte:
                distance_voisin_fin = calc_distance(G.nodes[i], G.nodes[fin])
                liste_ouverte.append(i)
                distances[i] = distance_voisin_fin
                sommet_precedent[i] = sommet_actuel
            #Si il n'est pas déjà dans la liste des possibilité,
            #on le rajoute ainsi que sa distance au sommet d'arrivée

        sommets_marques.append(sommet_actuel)
        liste_ouverte.remove(sommet_actuel)

        plus_petit = float('inf')
        for k in liste_ouverte:
            proximitee = distances[sommet_precedent[k]] - distances[k]
            #Calcul du rapprochement gagné vers l'arrivée entre les sommets
            ratio = G.edges[(sommet_precedent[k], k, 0)]["length"]/proximitee
            #On détermine le ratio entre a quelle point cela nous rapproche
            #de l'arrivée et le coût du chemin.
            if proximitee > 0 and (ratio < plus_petit or plus_petit <= 0):
                plus_petit = ratio
                dernier = k
            #Si le ratio est plus petit que le précédent on est le màj
            elif proximitee <= 0 and (plus_petit == float('inf') 
                                 or ratio > plus_petit):
                plus_petit = ratio
                dernier = k
            #Dans le cas où la proximitée est négative, 
            #le processus est inversée, ainsi, 
            # si le ratio est plus grand que le précédent on est le màj
        
        sommet_actuel = dernier
        #Mise à jour du sommet actuel
    
    return fin_algo(sommet_precedent, 
                    plus_petit == float('inf'), debut, fin)