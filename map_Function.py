import folium as fo
import osmnx as ox
import geocoder
import custom_algo_pf as ca

def name_To_Graphml(name):
    print("Map en cours de téléchargement")
    # Affichage des logs de la console
    ox.config(log_console=False)

    # Telecharge la carte et retourne un MultiDiGraph
    G = ox.graph_from_address(name, network_type='all') # network_type = {"all_private", "all", "bike", "drive", "drive_service", "walk"}

    # Sauvegarde la carte dans le dossier graphml
    print("Map Téléchargé")
    return G

def Graphml_to_Html(name, graph):
    print(type(name))
    node = graph.nodes(data=True)

    orig1 = list(node)[0][0]
    dest1 = list(node)[-1][0]

    routes = ca.opti_dijkstra(graph, orig1, dest1)
    x = ox.folium.plot_route_folium(graph,routes)

    fo.Marker([float(list(node)[0][1]['y']),float(list(node)[0][1]['x'])], popup='Départ',icon=fo.Icon(color="red", icon="glyphicon glyphicon-map-marker",popup="Départ"), draggable=True).add_to(x)
    fo.Marker([float(list(node)[-1][1]['y']),float(list(node)[-1][1]['x'])],icon=fo.Icon(color="green", icon="glyphicon glyphicon-record", popup="Arrivé"), draggable=True).add_to(x)

    x.save("map.html")