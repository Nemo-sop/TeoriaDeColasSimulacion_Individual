"""
eventos:
    En Informes:
        1) Ingreso para informes                    (II)     - dist uniforme 8-12 minutos   / 480-720
        2) Llegada a informes                       (LI)     - dist uniforme 3-7 segundos
        3) Fin atencion informes                    (FI)     - dist uniforme 4-14 minutos   / 240-840
        4) Llegada a la puerta desde informes       (LPI)     - dist uniforme 15-25 segundos

    En Reservas:
        1) Llegada a reservas desde informes        (LRI)    - dist uniforme 5-15 segundos
        2) Fin atencion reservas                    (FR)     - dist uniforme 5-9 minutos    / 300-540
        3) Ingreso para reservas                    (IR)     - dist uniforme 12-18 minutos  / 720-1080
        4) Llegada a reservas                       (LR)     - dist uniforme 12-18 segundos
        5) Llegada a la puerta desde reservas       (LPR)    - dist uniforme 15-25 segundos

    Interrupciones:
        1) Inicio alarma                            (IA)     - dist uniforme 160-200 minutos  / 9600-12000
        2) Fin alarma                                        - ecdif (asumo q t=1min --> multiplico por 60)

def simular(0, 2000, 480, 720, 3, 7, 240, 840, 15, 25, 5, 15, 300, 540, 720, 1000, 12, 18, 15, 25):
"""
import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication

from Objetos.Evento import Evento
from Objetos.Persona import Persona
from Objetos.Servidores import Servidor
from RungeKutta.RungeKutta import calcularRK
from distribuciones import *
import bisect

def simular(pantalla, filaInicio, finSimulacion, aII, bII, aLI, bLI, aFI, bFI, aLPI, bLPI, aLRI, bLRI, aFR, bFR, aIR, bIR, aLR, bLR, aLPR, bLPR, aIA, bIA):
    # Inicializamos todos los objetos permanentes y el dataframe
    filaInicio = filaInicio

    tabla = pd.DataFrame({"Reloj":[], "Tipo De Evento":[], "Nombre":[],
                          "Tiempo Hasta La Proxima Llegada para informes":[], "Proxima Llegada informes":[],
                          "Tiempo Hasta La Proxima Llegada para reservas":[], "Proxima Llegada reservas":[],
                          "Proximo Ataque":[], "Duracion del Ataque":[],
                          "Estado Informes":[], "Informes ocupado por":[],  "Cola Informes":[], "Estado Reservas":[], "Reservas ocupado por":[],"Cola Reservas":[],
                          "Tiempo oscioso informes":[], "Tiempo oscioso reservas":[], "Porcentaje de trabajo de alarmas":[],
                          "Atendidos en informes":[], "Atendidos en reservas":[],
                          "Cantidad de personas esperando":[], "Cantidad de personas atendidas":[]})


    servidorInformes = Servidor("Informes", "Libre", [], 0, 0)
    servidorReservas = Servidor("Reservas", "Libre", [], 0, 0)
    eventos = []
    reloj = 0
    porcentajeDeTrabajoAlarma = 0
    nroDeFila = 0
    RKCalculado = False


    # Inizializamos las primeras llegadas

    primeraIngresoInformes = Evento("Ingreso para informes", tiempo(aII, bII), Persona())
    primeraIngresoReservas = Evento("Ingreso para reservas", tiempo(aIR, bIR), Persona())

    persona = Persona()
    primerAtque = Evento("Inicio alarma", tiempo(aIR, bIR), persona.anular())


    bisect.insort_right(eventos, primeraIngresoReservas)
    bisect.insort_right(eventos, primeraIngresoInformes)
    bisect.insort_right(eventos, primerAtque)


    while reloj < finSimulacion:
        print(reloj)

        eventoActual = eventos[0]
        reloj = eventoActual.get_tiempo()

        if eventoActual.get_tipoEvento() == "Ingreso para informes":

            llegadaDelIngreso = Evento("Llegada a informes", tiempo(aLI, bLI) + reloj, eventoActual.get_persona())
            nuevoIngreso = Evento("Ingreso para informes", tiempo(aII, bII) + reloj, Persona())
            bisect.insort_right(eventos, llegadaDelIngreso)
            bisect.insort_right(eventos, nuevoIngreso)

        elif eventoActual.get_tipoEvento() == "Llegada a informes":

            if servidorInformes.get_estado() == "Libre":
                servidorInformes.set_estado("Ocupado")
                servidorInformes.set_siendoAtendido(eventoActual.get_persona())
                finAtencionInforme = Evento("Fin atencion informes", tiempo(aFI, bFI) + reloj,eventoActual.get_persona())
                bisect.insort_right(eventos, finAtencionInforme)
                servidorInformes.add_tiempoOscioso(reloj - servidorInformes.get_seDesocupo())
                servidorInformes.reiniciar_seDesocupo()
            else:
                servidorInformes.add_cola(eventoActual.get_persona())

        elif eventoActual.get_tipoEvento() == "Fin atencion informes":

            if len(servidorInformes.get_cola()) == 0:
                servidorInformes.set_estado("Libre")
                servidorInformes.set_siendoAtendido("Nadie")
                servidorInformes.set_seDesocupo(reloj)
            else:
                finAtencionInforme = Evento("Fin atencion informes", tiempo(aFI, bFI) + reloj, servidorInformes.get_elQueSigue())
                servidorInformes.set_siendoAtendido(servidorInformes.get_elQueSigue())
                servidorReservas.mover_cola()
                bisect.insort_right(eventos, finAtencionInforme)

            servidorInformes.agregarAtendido()
            if random.random() < 0.6:
                salidaPorLaPuerta = Evento("Llegada a la puerta desde informes", tiempo(aLPI, bLPI) + reloj, eventoActual.get_persona())
                bisect.insort_right(eventos, salidaPorLaPuerta)
            else:
                irAReservas = Evento("Llegada a reservas desde informes", tiempo(aLRI, bLRI) + reloj, eventoActual.get_persona())
                bisect.insort_right(eventos, irAReservas)

        elif eventoActual.get_tipoEvento() == "Llegada a la puerta desde informes":
            pass
        elif eventoActual.get_tipoEvento() == "Llegada a la puerta desde informes":
            pass
        elif eventoActual.get_tipoEvento() == "Llegada a reservas desde informes":

            if servidorReservas.get_estado() == "Libre":
                servidorReservas.set_estado("Ocupado")
                servidorReservas.set_siendoAtendido(eventoActual.get_persona())
                finAtencionReservas = Evento("Fin atencion reservas", tiempo(aFR, bFR) + reloj, eventoActual.get_persona())
                bisect.insort_right(eventos, finAtencionReservas)
                servidorReservas.add_tiempoOscioso(reloj - servidorReservas.get_seDesocupo())
                servidorReservas.reiniciar_seDesocupo()
            else:
                servidorReservas.add_cola(eventoActual.get_persona())

        elif eventoActual.get_tipoEvento() == "Fin atencion reservas":

            if len(servidorReservas.get_cola()) == 0:
                servidorReservas.set_estado("Libre")
                servidorReservas.set_siendoAtendido("Nadie")
                servidorReservas.set_seDesocupo(reloj)
            else:
                finAtencionReservas = Evento("Fin atencion reservas", tiempo(aFR, bFR) + reloj, servidorReservas.get_elQueSigue())
                servidorReservas.set_siendoAtendido(servidorReservas.get_elQueSigue())
                servidorReservas.mover_cola()
                bisect.insort_right(eventos, finAtencionReservas)

            salidaPorLaPuerta = Evento("Llegada a la puerta desde reservas", tiempo(aLPR, bLPR) + reloj, eventoActual.get_persona())
            bisect.insort_right(eventos, salidaPorLaPuerta)

        elif eventoActual.get_tipoEvento() == "Ingreso para reservas":

            llegadaDelIngreso = Evento("Llegada a reservas", tiempo(aLR, bLR) + reloj, eventoActual.get_persona())
            nuevoIngreso = Evento("Ingreso para reservas", tiempo(aIR, bIR) + reloj, Persona())
            bisect.insort_right(eventos, llegadaDelIngreso)
            bisect.insort_right(eventos, nuevoIngreso)

        elif eventoActual.get_tipoEvento() == "Llegada a reservas":

            if servidorReservas.get_estado() == "Libre":
                servidorReservas.set_estado("Ocupado")
                finAtencionReservas = Evento("Fin atencion reservas", tiempo(aFR, bFR) + reloj,eventoActual.get_persona())
                bisect.insort_right(eventos, finAtencionReservas)
                servidorReservas.add_tiempoOscioso(reloj - servidorReservas.get_seDesocupo())
                servidorReservas.reiniciar_seDesocupo()
            else:
                servidorReservas.add_cola(eventoActual.get_persona())

        elif eventoActual.get_tipoEvento() == "Inicio alarma":

            servidorReservas.set_estado("Atacado")
            servidorInformes.set_estado("Atacado")

            persona = Persona()

            if not RKCalculado:
                valor, dfRungeKutta = calcularRK()
                RKCalculado = True

            finAlarma = Evento("Fin alarma", valor + reloj, persona.anular())
            bisect.insort_right(eventos, finAlarma)

            for i in eventos:
                if i.get_tipoEvento() == "Fin atencion informes" or i.get_tipoEvento() == "Fin atencion reservas":
                    i.add_tiempo(valor)


        elif eventoActual.get_tipoEvento() == "Fin alarma":
            persona = Persona()
            proximoAtaque = Evento("Inicio alarma", tiempo(aIA, bIA) + reloj, persona.anular())
            bisect.insort_right(eventos, proximoAtaque)

        else:
            print("Algo hiciste mal...")

        fila = pd.DataFrame({"Reloj": [], "Tipo De Evento": [], "Nombre": [],
                              "Tiempo Hasta La Proxima Llegada para informes": [], "Proxima Llegada informes": [],
                              "Tiempo Hasta La Proxima Llegada para reservas": [], "Proxima Llegada reservas": [],
                              "Proximo Ataque": [], "Duracion del Ataque": [],
                              "Estado Informes": [], "Informes ocupado por": [], "Cola Informes": [],
                              "Estado Reservas": [], "Reservas ocupado por": [], "Cola Reservas": [],
                              "Tiempo oscioso informes": [], "Tiempo oscioso reservas": [],
                              "Porcentaje de trabajo de alarmas": [],
                              "Atendidos en informes": [], "Atendidos en reservas": [],
                              "Cantidad de personas esperando": [], "Cantidad de personas atendidas": []})


        # Construimos el dataframe

        if True:#filaInicio < nroDeFila and nroDeFila < 400 + filaInicio:
            fila.at[0, "Reloj"] = reloj
            fila.at[0, "Tipo De Evento"] = reloj
            fila.at[0, "Nombre"] = reloj
            fila.at[0, "Tiempo Hasta La Proxima Llegada para informes"] = reloj
            fila.at[0, "Proxima Llegada informes"] = reloj
            fila.at[0, "Tiempo Hasta La Proxima Llegada para reservas"] = reloj
            fila.at[0, "Proxima Llegada reservas"] = reloj
            fila.at[0, "Proximo Ataque"] = reloj
            fila.at[0, "Duracion del Ataque"] = reloj
            fila.at[0, "Estado Informes"] = reloj
            fila.at[0, "Informes ocupado por"] = reloj
            fila.at[0, "Cola Informes"] = reloj
            fila.at[0, "Estado Reservas"] = reloj
            fila.at[0, "Reservas ocupado por"] = reloj
            fila.at[0, "Cola Reservas"] = reloj
            fila.at[0, "Tiempo oscioso informes"] = reloj
            fila.at[0, "Tiempo oscioso reservas"] = reloj
            fila.at[0, "Porcentaje de trabajo de alarmas"] = reloj
            fila.at[0, "Atendidos en informes"] = reloj
            fila.at[0, "Atendidos en reservas"] = reloj
            fila.at[0, "Cantidad de personas esperando"] = reloj
            fila.at[0, "Cantidad de personas atendidas"] = reloj




        eventos.remove(eventoActual)
        tabla = pd.concat([tabla, fila], ignore_index=True)
        nroDeFila += 1

    print("Llegue aca")

    pantalla.mostrarResultados(tabla, dfRungeKutta)

    return tabla, dfRungeKutta

# x, y = simular(0, 2000, 480, 720, 3, 7, 240, 840, 15, 25, 5, 15, 300, 540, 720, 1000, 12, 18, 15, 25, 9600, 12000)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# print(x)





