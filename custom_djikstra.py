import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox


def custom_dijkstra(G, start, finish):

    print("Lancement de dijkstra custom :")
    
    distances = {} #On initialise le dictionnaire notant la distance du point d'origine pour chaque sommets
    previous_nodes = {} #On initialise le dictionnaire notant le sommet précédant du sommet en question
    smallest_path = [] #Une liste des sommets à emprunter pour effectuer le chemin le plus court

    unvisited_nodes = list(nx.nodes(G)) #On récupère tout les sommets (qui plus tard représentera tous les sommets non visité par l'algo)

    for i in unvisited_nodes:
        distances[i] = float('inf') #On initialise la distance du départ au sommet en question à infini

    current = start # Création de la variable "current" qui correspond au sommet actuellement "analysé" par l'algo   
    distances[current] = 0  # Le point de départ est par définition à une distance de 0 de lui même
    previous_nodes[start] = None #Il n'a pas de sommet précédent


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

        unvisited_nodes.remove(current) #On retire le sommet actuel des visités
        current = last #On affecte le nouveau sommet qui a la plus petit distance avec le départ en tant que sommet actuel

    #On remonte le dictionnaire du sommet précédent afin de récupérer quelle sommets emprunter afin de prendre le trajet le plus cours
    boolean = True
    while boolean:
        smallest_path.insert(0, finish)
        finish = previous_nodes[finish]
        if finish == None:
            boolean = False

    print("Fin de dijkstra custom")
    return smallest_path