import sys
import os
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings

from PySide6.QtWidgets import (QApplication, QComboBox, QLineEdit,
                               QMainWindow, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from PySide6.QtWebEngineWidgets import QWebEngineView

import map_Function

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.creation_telechargement()
        self.creation_selection_trajet()
        self.creation_traject_visualiser()

        self.stack_widget = QStackedWidget(self)
        self.stack_widget.addWidget(self.stack1)
        self.stack_widget.addWidget(self.stack2)
        self.stack_widget.addWidget(self.stack3)
        self.setCentralWidget(self.stack_widget)
        self.show()

    def creation_telechargement(self):
        self.addresse_ville = QLineEdit()
        self.addresse_ville.setPlaceholderText("Emplacement a télecharger")
        self.Q_boutton_telechargement = QPushButton("Télécharger la carte")
        self.Q_boutton_telechargement.clicked.connect(self.fonction_1)
        
        # Layout 
        layout1 = QVBoxLayout()
        layout1.addWidget(self.addresse_ville)
        layout1.addWidget(self.Q_boutton_telechargement)
        self.stack1.setLayout(layout1)
    
    def creation_selection_trajet(self):
        self.Q_combobox_depart = QComboBox()
        self.Q_combobox_arrive = QComboBox()
        self.Q_boutton_telechargement = QPushButton("Telecharger la carte")
        self.Q_boutton_telechargement.clicked.connect(self.fonction_2)
        
        self.carte_visualiser = QWebEngineView()
        self.path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "map.html")
        self.carte_visualiser.load(QUrl.fromLocalFile(self.path))
        self.carte_visualiser.show()

        layout2 = QVBoxLayout()
        layout2.addWidget(self.Q_combobox_depart)
        layout2.addWidget(self.Q_combobox_arrive)
        layout2.addWidget(self.Q_boutton_telechargement)

        layout2.addWidget(self.carte_visualiser)
        self.stack2.setLayout(layout2)
    
    def creation_traject_visualiser(self):
        self.carte_visualiser2 = QWebEngineView()
        self.carte_visualiser2.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)
        self.carte_visualiser2.load(QUrl.fromLocalFile(self.path))
        self.carte_visualiser2.show()

        layout3 = QVBoxLayout()
        layout3.addWidget(self.carte_visualiser2)
        self.stack3.setLayout(layout3)

    def fonction_1(self):
        self.adresse = self.addresse_ville.text()
        self.graph = map_Function.name_To_Graphml(self.adresse)
        map_Function.Graphml_to_Html(self.graph)
        self.carte_visualiser.reload()

        self.adresse_liste = map_Function.trouve_adresse_liste(self.graph)

        for i in range(len(self.adresse_liste)):
            self.Q_combobox_arrive.addItem(self.adresse_liste[i][0],self.adresse_liste[i][1])
            self.Q_combobox_depart.addItem(self.adresse_liste[i][0],self.adresse_liste[i][1])

        
        print(self.Q_combobox_arrive.currentData())
        print(self.Q_combobox_arrive.currentText())


        self.stack_widget.setCurrentIndex(1)

    def fonction_2(self):

        self.id_depart = self.Q_combobox_depart.currentData()
        self.txt_depart = self.Q_combobox_depart.currentText()

        self.id_arrive = self.Q_combobox_arrive.currentData()
        self.txt_arrive = self.Q_combobox_arrive.currentText()

        map_Function.adresse_en_html(self.graph, self.id_depart, self.id_arrive)


        self.carte_visualiser2.reload()



        self.stack_widget.setCurrentIndex(2)
        

application = QApplication(sys.argv)
fenetre = MainWindow()
fenetre.show()
application.exec()
