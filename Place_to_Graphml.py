import osmnx as ox

place = input("Adresse : ")
filename = input("Nom Fichier : ")

# Affichage des logs de la console
ox.config(log_console=True)


# Telecharge la carte et retourne un MultiDiGraph
G = ox.graph_from_address(place, network_type='walk') # network_type = {"all_private", "all", "bike", "drive", "drive_service", "walk"}


# Sauvegarde la carte dans le dossier graphml
ox.save_graphml(G,'graphml/'+filename+'.graphml')
print ('Fichier Crée')