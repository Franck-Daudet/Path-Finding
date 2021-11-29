import os
import sys
from PySide2 import QtWidgets
from PySide2.QtCore import QUrl, Slot
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget
import map_Function
import folium

app = QApplication(sys.argv)
window = QWidget()
buttonDownloader = QtWidgets.QPushButton("Télécharger une nouvelle map")
villeDownloader = QtWidgets.QLineEdit()
villeDownloader.setPlaceholderText("Télécharger la carte")

webmap = QWebEngineView()

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map.html")
webmap.load(QUrl.fromLocalFile(path))

#Layout
layout = QGridLayout()
layout.addWidget(buttonDownloader, 0, 0)
layout.addWidget(villeDownloader, 1, 0)
layout.addWidget(webmap, 2, 0)
window.setLayout(layout)

@Slot()
def on_click():
    global G
    G = map_Function.name_To_Graphml(villeDownloader.text())
    map_Function.Graphml_to_Html(villeDownloader.text(), G)
    webmap.reload()



buttonDownloader.clicked.connect(on_click)

window.show()
app.exec_()