import folium as fo
import osmnx as ox
import custom_algo_pf as ca

def addresse_en_graph(adresse, type_graph):
    '''Prend en paramètre une adresse et retourne un graph'''
    print("Map en cours de téléchargement")
    # Affichage des logs de la console
    ox.config(log_console=False)

    # Telecharge la carte et retourne un MultiDiGraph
    graphml = ox.graph_from_address(adresse, network_type=type_graph) # network_type = {"all_private", "all", "bike", "drive", "drive_service", "walk"}

    print("Map Téléchargé")
    return graphml

def graph_to_html(graph):
    '''Récupère un graph en paramètre et le convertit en map.html'''
    x = ox.plot_graph_folium(graph)
    x.save("map.html")


def trouve_adresse_liste(graphml):
    '''Recherche la liste des adresses existantes dans le graph
    Le graph contient une liste d'adresse de la forme [adresse, id_node]
    '''
    adresse_liste = [] # Liste des adresses du graph
    adresse_temp = []
    for elt in graphml.edges(data='name') : # data='name' retourne une tuple (NodeId, NodeId, adresse) si adresse non spécifié adresse = None
        string = str(elt[2])
        if(string != 'None' and string not in adresse_temp):
            # string.startswith('[') permet de supprimer les adresse "ambigues" (ex: ['Traverse de la Savoisienne', 'Traverse des Pénitents Noirs'])
            if (not(string.startswith('['))):
                adresse_liste.append([string , elt[0]])
                adresse_temp.append(string)
    adresse_liste.sort()
    return adresse_liste

def trajet_en_html(graph, node_depart, node_arrive,algorithme):
    '''Récupère un graph en paramètre ainsi que le node d'arrivé et de départ,
    utilise un algorithme de recherche et retourne un map.html
    '''
    route = getattr(ca, algorithme)(graph, node_depart, node_arrive)
    x = ox.folium.plot_route_folium(graph,route)

    position_depart = graph.nodes[node_depart]
    position_arrive = graph.nodes[node_arrive]

    fo.Marker(
             (position_depart['y'],position_depart['x']),
             icon=fo.Icon(color="red"),
             popup="Départ").add_to(x)

    fo.Marker(
             (position_arrive['y'],position_arrive['x']),
             icon=fo.Icon(color="green"),
             popup="Arrivé").add_to(x)


    x.save("map.html")