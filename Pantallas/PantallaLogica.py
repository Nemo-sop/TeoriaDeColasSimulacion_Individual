from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class Pantalla(QMainWindow):
    """Incializar clase"""

    def __init__(self):
        super().__init__()

        """Cargar la GUI"""
        uic.loadUi("Pantallas/Pantalla.ui", self)

        #self.btn_simular.clicked.connect()