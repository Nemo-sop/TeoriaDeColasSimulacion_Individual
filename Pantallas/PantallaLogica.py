from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from Auxiliar import simular


class Pantalla(QMainWindow):
    """Incializar clase"""

    def __init__(self):
        super().__init__()

        """Cargar la GUI"""
        uic.loadUi("Pantallas/Pantalla.ui", self)

        self.btn_simular.clicked.connect(self.metodoAuxiliar)

    def metodoAuxiliar(self):

        if self.duracion.text() != "":
            simular(self, int(self.inicio.text()), int(self.duracion.text()), int(self.probIrReservas.text()), int(self.aII.text()), int(self.bII.text()), int(self.aLI.text()),
                    int(self.bLI.text()), int(self.aFI.text()), int(self.bFI.text()), int(self.aLPI.text()), int(self.bLPI.text()), int(self.aLRI.text()),
                    int(self.bLRI.text()), int(self.aFR.text()), int(self.bFR.text()), int(self.aIR.text()), int(self.bIR.text()), int(self.aLR.text()),
                    int(self.bLR.text()), int(self.aLPR.text()), int(self.bLPR.text()), int(self.aIA.text()), int(self.bIA.text()))


    def mostrarResultados(self, tabla, tablaRK):
        #print(tabla)

        fila = 0
        self.tablaSimulacion.setRowCount(len(tabla))
        for i in range(len(tabla)):
            self.tablaSimulacion.setItem(fila, 0 , QTableWidgetItem(str(tabla.at[i, "Reloj"])))
            self.tablaSimulacion.setItem(fila, 1 , QTableWidgetItem(str(tabla.at[i, "Tipo De Evento"])))
            self.tablaSimulacion.setItem(fila, 2 , QTableWidgetItem(str(tabla.at[i, "Nombre"])))
            self.tablaSimulacion.setItem(fila, 3 , QTableWidgetItem(str(tabla.at[i, "Tiempo Hasta La Proxima Llegada para informes"])))
            self.tablaSimulacion.setItem(fila, 4 , QTableWidgetItem(str(tabla.at[i, "Proxima Llegada informes"])))
            self.tablaSimulacion.setItem(fila, 5 , QTableWidgetItem(str(tabla.at[i, "Tiempo Hasta La Proxima Llegada para reservas"])))
            self.tablaSimulacion.setItem(fila, 6 , QTableWidgetItem(str(tabla.at[i, "Proxima Llegada reservas"])))
            self.tablaSimulacion.setItem(fila, 7 , QTableWidgetItem(str(tabla.at[i, "Proximo Ataque"])))
            self.tablaSimulacion.setItem(fila, 8 , QTableWidgetItem(str(tabla.at[i, "Duracion del Ataque"])))
            self.tablaSimulacion.setItem(fila, 9 , QTableWidgetItem(str(tabla.at[i, "Estado Informes"])))
            self.tablaSimulacion.setItem(fila, 10, QTableWidgetItem(str(tabla.at[i, "Informes ocupado por"])))
            self.tablaSimulacion.setItem(fila, 11, QTableWidgetItem(str(tabla.at[i, "Cola Informes"])))
            self.tablaSimulacion.setItem(fila, 12, QTableWidgetItem(str(tabla.at[i, "Estado Reservas"])))
            self.tablaSimulacion.setItem(fila, 13, QTableWidgetItem(str(tabla.at[i, "Reservas ocupado por"])))
            self.tablaSimulacion.setItem(fila, 14, QTableWidgetItem(str(tabla.at[i, "Cola Reservas"])))
            self.tablaSimulacion.setItem(fila, 15, QTableWidgetItem(str(tabla.at[i, "Tiempo oscioso informes"])))
            self.tablaSimulacion.setItem(fila, 16, QTableWidgetItem(str(tabla.at[i, "Tiempo oscioso reservas"])))
            self.tablaSimulacion.setItem(fila, 17, QTableWidgetItem(str(tabla.at[i, "Porcentaje de trabajo de alarmas"])))
            self.tablaSimulacion.setItem(fila, 18, QTableWidgetItem(str(tabla.at[i, "Atendidos en informes"])))
            self.tablaSimulacion.setItem(fila, 19, QTableWidgetItem(str(tabla.at[i, "Atendidos en reservas"])))
            self.tablaSimulacion.setItem(fila, 20, QTableWidgetItem(str(tabla.at[i, "Cantidad de personas esperando"])))
            self.tablaSimulacion.setItem(fila, 21, QTableWidgetItem(str(tabla.at[i, "Cantidad de personas atendidas"])))

            fila += 1
        # Cargamos la tabla del RK
        filaRK = 0
        self.tablaRK.setRowCount(len(tablaRK))
        for i in range(len(tablaRK)):
            self.tablaRK.setItem(filaRK, 0, QTableWidgetItem(str(round(tablaRK.at[i, "xi"], 4))))
            self.tablaRK.setItem(filaRK, 1, QTableWidgetItem(str(round(tablaRK.at[i, "yi"], 4))))
            self.tablaRK.setItem(filaRK, 2, QTableWidgetItem(str(round(tablaRK.at[i, "k1"], 4))))
            self.tablaRK.setItem(filaRK, 3, QTableWidgetItem(str(round(tablaRK.at[i, "k2"], 4))))
            self.tablaRK.setItem(filaRK, 4, QTableWidgetItem(str(round(tablaRK.at[i, "k3"], 4))))
            self.tablaRK.setItem(filaRK, 5, QTableWidgetItem(str(round(tablaRK.at[i, "k4"], 4))))
            self.tablaRK.setItem(filaRK, 6, QTableWidgetItem(str(round(tablaRK.at[i, "xi+1"], 4))))
            self.tablaRK.setItem(filaRK, 7, QTableWidgetItem(str(round(tablaRK.at[i, "yi+1"], 4))))

            filaRK += 1