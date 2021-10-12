import osmnx as ox
import networkx as nx

filename = input("Nom du fichier .graphml : ")

G = ox.load_graphml('graphml/' + filename + '.graphml')
G = ox.bearing.add_edge_bearings(G, precision=1)

ox.plot_graph(G)