import folium as fo
from numpy import matrix
import osmnx as ox
import custom_algo_pf as ca

def name_To_Graphml(name):
    print("Map en cours de téléchargement")
    # Affichage des logs de la console
    ox.config(log_console=False)

    # Telecharge la carte et retourne un MultiDiGraph
    graphml = ox.graph_from_address(name, network_type='all') # network_type = {"all_private", "all", "bike", "drive", "drive_service", "walk"}

    print("Map Téléchargé")
    return graphml

def Graphml_to_Html(graph):
    x = ox.plot_graph_folium(graph)
    x.save("map.html")

def route_to_Html(graph,node_depart, node_arrive):
    print(node_depart)
    print(node_arrive)

    x = ox.plot_graph_folium(graph)
    x.save("map.html")

def trouve_adresse_liste(graphml):
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

def adresse_en_html(graph, node_depart, node_arrive):
    route = ca.custom_dijkstra(graph, node_depart, node_arrive)
    x = ox.folium.plot_route_folium(graph,route)

    # for i in range(len(route)-1):
    #     print(graph[route[i]][route[i+1]])
    position_depart = graph.node[node_depart]
    position_arrive = graph.node[node_arrive]

    fo.Marker(
             (position_depart['y'],position_depart['x']),
             icon=fo.Icon(color="red"),
             popup="Départ").add_to(x)

    fo.Marker(
             (position_arrive['y'],position_arrive['x']),
             icon=fo.Icon(color="green"),
             popup="Arrivé").add_to(x)


    x.save("map.html")