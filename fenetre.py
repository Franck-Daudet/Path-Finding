import sys
import os
from PySide6.QtCore import QSize, QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings

from PySide6.QtWidgets import (QApplication, QComboBox, QLineEdit,
                               QMainWindow, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from PySide6.QtWebEngineWidgets import QWebEngineView

import map_Function

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        #Initialisation des 3 fenetres
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        #Ajout des widgets et configuration de la fenetre
        self.creation_telechargement()
        self.creation_selection_trajet()
        self.creation_traject_visualiser()
        
        #Création d'un stackedWidget permettant de gerer le changement de fenetre
        self.stack_widget = QStackedWidget(self)
        self.stack_widget.addWidget(self.stack1)
        self.stack_widget.addWidget(self.stack2)
        self.stack_widget.addWidget(self.stack3)

        #Ajout du stackWidget dans la fenetre
        self.setCentralWidget(self.stack_widget)
        #affichage de la fenetre   
        self.show()

    def creation_telechargement(self):
        #Création des widgets
        self.addresse_ville = QLineEdit()
        self.addresse_ville.setPlaceholderText("Quelle carte faut-il télecharger")
        self.Q_boutton_telechargement = QPushButton("Télécharger la carte")
        #Ajout de la fonction au click sur le bouton 
        self.Q_boutton_telechargement.clicked.connect(self.fonction_1)
        
        #Agencement de la fentre
        layout1 = QVBoxLayout()
        layout1.addWidget(self.addresse_ville)
        layout1.addWidget(self.Q_boutton_telechargement)
        self.stack1.setLayout(layout1)
    
    def creation_selection_trajet(self):
        #Création des widgets
        self.Q_combobox_depart = QComboBox()
        self.Q_combobox_arrive = QComboBox()
        self.Q_boutton_telechargement = QPushButton("Telecharger la carte")
        self.Q_boutton_telechargement.clicked.connect(self.fonction_2)
        
        #Création de la fentre de visualisation web
        self.carte_visualiser = QWebEngineView()
        self.carte_visualiser.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)

        #La variable path va retourner le chemin vers map.html
        self.path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "map.html")
        self.carte_visualiser.load(QUrl.fromLocalFile(self.path))
        self.carte_visualiser.show()

        #Agencement de la fentre
        layout2 = QVBoxLayout()
        layout2.addWidget(self.Q_combobox_depart)
        layout2.addWidget(self.Q_combobox_arrive)
        layout2.addWidget(self.Q_boutton_telechargement)
        layout2.addWidget(self.carte_visualiser)
        self.stack2.setLayout(layout2)
    
    def creation_traject_visualiser(self):
        #Création des widgets
        self.carte_visualiser2 = QWebEngineView()
        self.carte_visualiser2.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)
        self.carte_visualiser2.load(QUrl.fromLocalFile(self.path))
        self.carte_visualiser2.show()

        #Agencement de la fentre
        layout3 = QVBoxLayout()
        layout3.addWidget(self.carte_visualiser2)
        self.stack3.setLayout(layout3)

    def fonction_1(self):    
        '''Cette fonction va s'activer sur le bouton de la 1ere fenetre, elle va :
            - Récuperer l'adresse écrite
            - Convertir cette adresse en Graph
            - Convertir ce graph en HTML
            - Recharger le visualiser web pour utiliser la nouvelle carte
            - Récuperer la liste d'adresse du graph et les inserer dans les 2 combobox
              pour chercher les adresse
            - Passer à la seconde fenetre
        '''
        self.adresse = self.addresse_ville.text()
        self.graph = map_Function.addresse_en_graph(self.adresse)
        map_Function.graph_to_html(self.graph)
        self.carte_visualiser.reload()

        self.adresse_liste = map_Function.trouve_adresse_liste(self.graph)

        for i in range(len(self.adresse_liste)):
            self.Q_combobox_arrive.addItem(self.adresse_liste[i][0],self.adresse_liste[i][1])
            self.Q_combobox_depart.addItem(self.adresse_liste[i][0],self.adresse_liste[i][1])

        self.stack_widget.setCurrentIndex(1)

    def fonction_2(self):
        '''Cette fonction va s'activer sur le bouton de la 2eme fenetre, elle va :
            - Récuperer les ID des nodes des adresses sélectionnées
            - Il va récuperer le graph et les 2 nodes pour créer la route entre les 2 points
            - Recharger le visualiser web pour utiliser la nouvelle carte
            - Passe à la 3eme fenetre
        '''
        self.id_depart = self.Q_combobox_depart.currentData()
        self.txt_depart = self.Q_combobox_depart.currentText()

        self.id_arrive = self.Q_combobox_arrive.currentData()
        self.txt_arrive = self.Q_combobox_arrive.currentText()

        map_Function.trajet_en_html(self.graph, self.id_depart, self.id_arrive)

        self.carte_visualiser2.reload()
        self.setFixedSize(QSize(700, 700))
        self.stack_widget.setCurrentIndex(2)
        

application = QApplication(sys.argv)
fenetre = MainWindow()
fenetre.show()
application.exec()
