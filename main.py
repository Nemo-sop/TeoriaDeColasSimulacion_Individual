import sys

from PyQt5.QtWidgets import QApplication

from Pantallas.PantallaLogica import Pantalla

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Pantalla()
    GUI.show()
    sys.exit(app.exec_())

