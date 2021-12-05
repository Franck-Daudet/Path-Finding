import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox

def calc_distance(a, b):
    return ((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2) ** 0.5

def dijkstra_loop(G, unvisited_nodes, distances, previous_nodes, start):
    
    current = start # Création de la variable "current" qui correspond au sommet actuellement "analysé" par l'algo
    distances[current] = 0  # Le point de départ est par définition à une distance de 0 de lui même

    while unvisited_nodes: #Exécute cette boucle tant qu'il y a des sommmets non visité
        neighbors_current = nx.neighbors(G, current) #On récupère tous les voisins du sommet actuel

        #On va affecter une distance entre le sommet actuel et les voisins si cette distance est plus petite que celle existante
        for j in neighbors_current:
            if j in unvisited_nodes:
                val = G.edges[(current, j, 0)]["length"] + distances[current]

                if distances[j] > val:
                    distances[j] = val
                    previous_nodes[j] = current

        
        smallest = float('inf')
        
        #On va sélectionner le sommet ayant une distance la plus petite avec le sommet de départ
        for k in distances:
            if k in unvisited_nodes and k != current:
                if smallest > distances[k]:
                    smallest = distances[k]
                    last = k
        
        unvisited_nodes.remove(current) #On retire   le sommet actuel des visités
        current = last #On affecte le nouveau sommet qui a la plus petit distance avec le départ en tant que sommet actuel
        if smallest == float('inf'): #Si le programme n'a pas trouvé de noeud ayant une distance non égale à l'infini, alors ces noeuds sont isolé du points de départ
            unvisited_nodes.clear()
    return previous_nodes

def custom_dijkstra(G, start, finish):

    print("Lancement de dijkstra custom :")
    
    distances = {} #On initialise le dictionnaire notant la distance du point d'origine pour chaque sommets
    previous_nodes = {} #On initialise le dictionnaire notant le sommet précédant du sommet en question
    smallest_path = [] #Une liste des sommets à emprunter pour effectuer le chemin le plus court

    unvisited_nodes = list(nx.nodes(G)) #On récupère tout les sommets (qui plus tard représentera tous les sommets non visité par l'algo)

    for i in unvisited_nodes:
        distances[i] = float('inf') #On initialise la distance du départ au sommet en question à infini

    previous_nodes[start] = None #Il n'a pas de sommet précédent
    previous_nodes[finish] = None #Tant qu'un chemin n'a pas été trouvé la valeur est null

    previous_nodes = dijkstra_loop(G, unvisited_nodes, distances, previous_nodes, start) 

    #On remonte le dictionnaire du sommet précédent afin de récupérer quelle sommets emprunter afin de prendre le trajet le plus cours
    if previous_nodes[finish] == None:
        print("Il n'existe pas de chemin pour atteindre ", finish, " depuis le point ", start)
        print("Fin de dijkstra custom")
        return []
    
    while finish != None:
        smallest_path.insert(0, finish)
        finish = previous_nodes[finish]

    print("Fin de dijkstra custom")
    return smallest_path


def opti_dijkstra(G, start, finish):

    print("Lancement de dijkstra opti :")
    
    distances = {} #On initialise le dictionnaire notant la distance du point d'origine pour chaque sommets
    previous_nodes = {} #On initialise le dictionnaire notant le sommet précédant du sommet en question
    smallest_path = [] #Une liste des sommets à emprunter pour effectuer le chemin le plus court

    unvisited_nodes = list(nx.nodes(G)) #On récupère tout les sommets (qui plus tard représentera tous les sommets non visité par l'algo)
    point_x = (G.nodes[start]['x'] + G.nodes[finish]['x'])/2
    point_y = (G.nodes[start]['y'] + G.nodes[finish]['y'])/2
    radius = calc_distance(G.nodes[start], {'x': point_x,'y': point_y}) * 1.25

    for j in unvisited_nodes:
        if calc_distance({'x': point_x,'y': point_y}, G.nodes[j]) > radius:
            unvisited_nodes.remove(j)
    
    for i in unvisited_nodes:
        distances[i] = float('inf') #On initialise la distance du départ au sommet en question à infini

    current = start # Création de la variable "current" qui correspond au sommet actuellement "analysé" par l'algo   
    distances[current] = 0  # Le point de départ est par définition à une distance de 0 de lui même
    previous_nodes[start] = None #Il n'a pas de sommet précédent
    previous_nodes[finish] = None #Tant qu'un chemin n'a pas été trouvé la valeur est null


    previous_nodes = dijkstra_loop(G, unvisited_nodes, distances, previous_nodes, start)
        
    #On remonte le dictionnaire du sommet précédent afin de récupérer quelle sommets emprunter afin de prendre le trajet le plus cours
    if previous_nodes[finish] == None:
        print("Il n'existe pas de chemin pour atteindre ", finish, " depuis le point ", start)
        print("Fin de dijkstra opti")
        return []
    
    while finish != None:
        smallest_path.insert(0, finish)
        finish = previous_nodes[finish]

    print("Fin de dijkstra opti")
    return smallest_path




def custom_Astar(G, start, finish):

    current = start

    previous_nodes = {}
    distances = {}
    smallest_path = []
    open_list = []
    marked = []

    
    current = start
    open_list.append(current)
    previous_nodes[current] = None
    distances[current] = calc_distance(G.nodes[start], G.nodes[finish])
    boolean = True

    while boolean:
        neighbors_current = list(nx.neighbors(G, current))
        for i in neighbors_current:
            if i == finish:
                previous_nodes[finish] = current
                boolean = False
                continue
            elif i not in marked:
                distance_neighbor_finish = calc_distance(G.nodes[i], G.nodes[finish])
                if i not in open_list:
                    open_list.append(i)
                    distances[i] = distance_neighbor_finish
                    previous_nodes[i] = current

        marked.append(current)
        open_list.remove(current)

        smallest = float('inf')
        for k in open_list:
            closer = distances[previous_nodes[k]] - distances[k]
            ratio = G.edges[(previous_nodes[k], k, 0)]["length"]/closer
            if closer > 0 and (ratio < smallest or smallest <= 0):
                smallest = ratio
                last = k
            elif closer <= 0 and (smallest == float('inf') or ratio > smallest):
                smallest = ratio
                last = k
    
        if smallest == float('inf'):
            print("Il n'existe pas de chemin pour atteindre ", finish, " depuis le point ", start)
            return []

        current = last

    while finish != None:
        smallest_path.insert(0, finish)
        finish = previous_nodes[finish]

    return smallest_path