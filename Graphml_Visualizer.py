import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
from custom_dijkstra import *

def main():
    filename = input("Nom du fichier .graphml : ")

    G = ox.load_graphml('path-finding/Path-Finding/graphml/' + filename + '.graphml')
    G = ox.bearing.add_edge_bearings(G, precision=1)
    
    ox.plot.plot_graph_route(G, custom_dijkstra(G, 26762546, 26762549), 'r')

if __name__ == "__main__":
    main()