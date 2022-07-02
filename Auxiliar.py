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

def simular(pantalla, filaInicio, finSimulacion, probIrReservas, aII, bII, aLI, bLI, aFI, bFI, aLPI, bLPI, aLRI, bLRI, aFR, bFR, aIR, bIR, aLR, bLR, aLPR, bLPR, aIA, bIA):
    # Inicializamos todos los objetos permanentes y el dataframe
    filaInicio = filaInicio

    tabla = pd.DataFrame({"Reloj":[], "Tipo De Evento":[], "Nombre":[], "Extra": [],
                          "Tiempo Hasta La Proxima Llegada para informes":[], "Proxima Llegada informes":[],
                          "Tiempo Hasta La Proxima Llegada para reservas":[], "Proxima Llegada reservas":[],
                          "Proximo Ataque":[], "Duracion del Ataque":[],
                          "Estado Informes":[], "Informes ocupado por":[],  "Cola Informes":[], "Estado Reservas":[], "Reservas ocupado por":[],"Cola Reservas":[],
                          "Tiempo oscioso informes":[], "Tiempo oscioso reservas":[], "Porcentaje de trabajo de alarmas":[],
                          "Atendidos en informes":[], "Atendidos en reservas":[],
                          "Cantidad de personas esperando":[], "Cantidad de personas atendidas":[]})


    colaInformes = []
    colaReservas = []
    servidorInformes = Servidor("Informes", "Libre", colaInformes, 0, 0)
    servidorReservas = Servidor("Reservas", "Libre", colaReservas, 0, 0)
    eventos = []
    reloj = 0
    tiempoDeTrabajoAlarma = 0
    nroDeFila = 0
    valorRK, dfRungeKutta = calcularRK()
    print(valorRK)



    # Inizializamos las primeras llegadas

    primeraIngresoInformes = Evento("Ingreso para informes", tiempo(aII, bII), Persona())
    primeraIngresoReservas = Evento("Ingreso para reservas", tiempo(aIR, bIR), Persona())

    persona = Persona()
    persona.anular()
    primerAtque = Evento("Inicio alarma", tiempo(aIA, bIA), persona)


    bisect.insort_right(eventos, primeraIngresoReservas)
    bisect.insort_right(eventos, primeraIngresoInformes)
    bisect.insort_right(eventos, primerAtque)


    while reloj < finSimulacion:


        eventoActual = eventos[0]
        reloj = eventoActual.get_tiempo()

        print(reloj, eventoActual.get_persona())

        if eventoActual.get_tipoEvento() == "Ingreso para informes":

            llegadaDelIngreso = Evento("Llegada a informes", tiempo(aLI, bLI) + reloj, eventoActual.get_persona())
            nuevoIngreso = Evento("Ingreso para informes", tiempo(aII, bII) + reloj, Persona())
            bisect.insort_right(eventos, llegadaDelIngreso)
            bisect.insort_right(eventos, nuevoIngreso)

        elif eventoActual.get_tipoEvento() == "Llegada a informes":

            if servidorInformes.get_estado() == "Libre":
                servidorInformes.set_estado("Ocupado")
                servidorInformes.set_siendoAtendido(eventoActual.get_persona().get_documento())
                finAtencionInforme = Evento("Fin atencion informes", tiempo(aFI, bFI) + reloj,eventoActual.get_persona())
                bisect.insort_right(eventos, finAtencionInforme)
                servidorInformes.add_tiempoOscioso(reloj - servidorInformes.get_seDesocupo())
                servidorInformes.reiniciar_seDesocupo()
            else:
                servidorInformes.add_cola(eventoActual.get_persona())

        elif eventoActual.get_tipoEvento() == "Fin atencion informes":

            if len(colaInformes) == 0:
                servidorInformes.set_estado("Libre")
                servidorInformes.set_siendoAtendido("Nadie")
                servidorInformes.set_seDesocupo(reloj)
            else:
                finAtencionInforme = Evento("Fin atencion informes", tiempo(aFI, bFI) + reloj, servidorInformes.get_elQueSigue())
                servidorInformes.set_siendoAtendido(servidorInformes.get_elQueSigue().get_documento())
                servidorInformes.mover_cola()
                #colaInformes.pop(0)
                bisect.insort_right(eventos, finAtencionInforme)

            servidorInformes.agregarAtendido()
            if random.random() < 1 - probIrReservas:
                vaAReservas = False
                salidaPorLaPuerta = Evento("Llegada a la puerta desde informes", tiempo(aLPI, bLPI) + reloj, eventoActual.get_persona())
                bisect.insort_right(eventos, salidaPorLaPuerta)
            else:
                vaAReservas = True
                irAReservas = Evento("Llegada a reservas desde informes", tiempo(aLRI, bLRI) + reloj, eventoActual.get_persona())
                bisect.insort_right(eventos, irAReservas)

        elif eventoActual.get_tipoEvento() == "Llegada a la puerta desde informes":
            pass
        elif eventoActual.get_tipoEvento() == "Llegada a la puerta desde reservas":
            pass
        elif eventoActual.get_tipoEvento() == "Llegada a reservas desde informes":

            if servidorReservas.get_estado() == "Libre":
                servidorReservas.set_estado("Ocupado")
                servidorReservas.set_siendoAtendido(eventoActual.get_persona().get_documento())
                finAtencionReservas = Evento("Fin atencion reservas", tiempo(aFR, bFR) + reloj, eventoActual.get_persona())
                bisect.insort_right(eventos, finAtencionReservas)
                servidorReservas.add_tiempoOscioso(reloj - servidorReservas.get_seDesocupo())
                servidorReservas.reiniciar_seDesocupo()
            else:
                servidorReservas.add_cola(eventoActual.get_persona())

        elif eventoActual.get_tipoEvento() == "Fin atencion reservas":

            if len(colaReservas) == 0:
                servidorReservas.set_estado("Libre")
                servidorReservas.set_siendoAtendido("Nadie")
                servidorReservas.set_seDesocupo(reloj)
            else:
                finAtencionReservas = Evento("Fin atencion reservas", tiempo(aFR, bFR) + reloj, servidorReservas.get_elQueSigue())
                servidorReservas.set_siendoAtendido(servidorReservas.get_elQueSigue().get_documento())
                servidorReservas.mover_cola()
                #colaReservas.pop(0)
                bisect.insort_right(eventos, finAtencionReservas)

            salidaPorLaPuerta = Evento("Llegada a la puerta desde reservas", tiempo(aLPR, bLPR) + reloj, eventoActual.get_persona())
            servidorReservas.agregarAtendido()
            bisect.insort_right(eventos, salidaPorLaPuerta)

        elif eventoActual.get_tipoEvento() == "Ingreso para reservas":

            llegadaDelIngreso = Evento("Llegada a reservas", tiempo(aLR, bLR) + reloj, eventoActual.get_persona())
            nuevoIngreso = Evento("Ingreso para reservas", tiempo(aIR, bIR) + reloj, Persona())
            bisect.insort_right(eventos, llegadaDelIngreso)
            bisect.insort_right(eventos, nuevoIngreso)

        elif eventoActual.get_tipoEvento() == "Llegada a reservas":

            if servidorReservas.get_estado() == "Libre":
                servidorReservas.set_estado("Ocupado")
                servidorReservas.set_siendoAtendido(eventoActual.get_persona().get_documento())
                finAtencionReservas = Evento("Fin atencion reservas", tiempo(aFR, bFR) + reloj,eventoActual.get_persona())
                bisect.insort_right(eventos, finAtencionReservas)
                servidorReservas.add_tiempoOscioso(reloj - servidorReservas.get_seDesocupo())
                servidorReservas.reiniciar_seDesocupo()
            else:
                servidorReservas.add_cola(eventoActual.get_persona())

        elif eventoActual.get_tipoEvento() == "Inicio alarma":

            servidorReservas.set_estado("Atacado")
            servidorInformes.set_estado("Atacado")

            tiempoDeTrabajoAlarma += valorRK

            persona = Persona()
            persona.anular()
            finAlarma = Evento("Fin alarma", valorRK + reloj, persona)
            bisect.insort_right(eventos, finAlarma)

            for i in eventos:
                if i.get_tipoEvento() == "Fin atencion informes" or i.get_tipoEvento() == "Fin atencion reservas":
                    i.add_tiempo(valorRK)


        elif eventoActual.get_tipoEvento() == "Fin alarma":

            persona = Persona()
            persona.anular()
            proximoAtaque = Evento("Inicio alarma", tiempo(aIA, bIA) + reloj, persona)
            bisect.insort_right(eventos, proximoAtaque)
            servidorReservas.set_estado(servidorReservas.get_estadoAnterior())
            servidorInformes.set_estado(servidorInformes.get_estadoAnterior())

        else:
            print("Algo hiciste mal...", eventoActual.get_tipoEvento())

        # Agergamos un extra que nos dice cuanto falta para el evento siguiente relacionado
        extra = " algo raro paso "
        demoraCaminar = 999
        if eventoActual.get_tipoEvento() == "Ingreso para informes":
            for i in eventos:

                if i.get_tipoEvento() == "Llegada a informes" and i.get_persona().get_documento() == eventoActual.get_persona().get_documento():
                    demoraCaminar = i.get_tiempo() - reloj

            extra = f"Tiempo en llegar a informes {demoraCaminar}"

        elif eventoActual.get_tipoEvento() == "Ingreso para reservas":
            for i in eventos:
                if i.get_tipoEvento() == "Llegada a reservas" and i.get_persona().get_documento() == eventoActual.get_persona().get_documento():
                    demoraCaminar = i.get_tiempo() - reloj

            extra = f"Tiempo en llegar a reservas {demoraCaminar}"

        elif eventoActual.get_tipoEvento() == "Llegada a informes":
            extra = "Se va a la cola"
            for i in eventos:
                if i.get_tipoEvento() == "Fin atencion informes" and i.get_persona().get_documento() == eventoActual.get_persona().get_documento():
                    extra = f"La atencion dura {i.get_tiempo() - reloj}"

        elif eventoActual.get_tipoEvento() == "Llegada a reservas" or eventoActual.get_tipoEvento() =="Llegada a reservas desde informes":
            extra = "Se va a la cola"
            for i in eventos:
                if i.get_tipoEvento() == "Fin atencion reservas" and i.get_persona().get_documento() == eventoActual.get_persona().get_documento():
                    extra = f"La atencion dura {i.get_tiempo() - reloj}"

        elif eventoActual.get_tipoEvento() == "Fin atencion informes":
            if vaAReservas:
                for i in range(len(eventos)):
                    print(demoraCaminar)
                    if eventos[i].get_tipoEvento() == "Llegada a reservas desde informes" and eventos[i].get_persona().get_documento() == eventoActual.get_persona().get_documento():
                        demoraCaminar = eventos[i].get_tiempo() - reloj

                extra = f"Tiempo en llegar a reservas desde informes {demoraCaminar}"
            else:
                for i in eventos:
                    if i.get_tipoEvento() == "Llegada a la puerta desde informes" and i.get_persona().get_documento() == eventoActual.get_persona().get_documento():
                        demoraCaminar = i.get_tiempo() - reloj

                extra = f"Tiempo en llegar a la puerta desde informes {demoraCaminar}"

        elif eventoActual.get_tipoEvento() == "Fin atencion reservas":
            for i in eventos:
                if i.get_tipoEvento() == "Llegada a la puerta desde reservas" and i.get_persona().get_documento() == eventoActual.get_persona().get_documento():
                    demoraCaminar = i.get_tiempo() - reloj

            extra = f"Tiempo en llegar a la puerta desde reservas {demoraCaminar}"

        elif eventoActual.get_tipoEvento() == "Fin atencion reservas":
            extra = f"La alarma de apagara en {valorRK} segundos"
        else:
            extra = "n/a"




        fila = pd.DataFrame({"Reloj": [], "Tipo De Evento": [], "Nombre": [], "Extra": [],
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
            fila.at[0, "Tipo De Evento"] = eventoActual.get_tipoEvento()
            fila.at[0, "Nombre"] = eventoActual.get_persona().get_documento()

            fila.at[0, "Extra"] = extra

            proximaLlegadaInformes = "no se calculo"
            proximaLlegadaReservas = "no se calculo"
            proximoAtaque = "no se calculo"
            finAtaque = "no se calculo"
            for i in eventos:
                if i.get_tipoEvento() == "Ingreso para informes":
                    proximaLlegadaInformes = i.get_tiempo()
                if i.get_tipoEvento() == "Ingreso para reservas":
                    proximaLlegadaReservas = i.get_tiempo()
                if i.get_tipoEvento() == "Inicio alarma":
                    proximoAtaque = i.get_tiempo()
                if i.get_tipoEvento() == "Fin alarma":
                    finAtaque = i.get_tiempo()


            fila.at[0, "Tiempo Hasta La Proxima Llegada para informes"] = proximaLlegadaInformes - reloj
            fila.at[0, "Proxima Llegada informes"] = proximaLlegadaInformes
            fila.at[0, "Tiempo Hasta La Proxima Llegada para reservas"] = proximaLlegadaReservas - reloj
            fila.at[0, "Proxima Llegada reservas"] = proximaLlegadaReservas
            fila.at[0, "Proximo Ataque"] =proximoAtaque
            if finAtaque == "no se calculo":
                fila.at[0, "Duracion del Ataque"] = "n/a"
            else:
                fila.at[0, "Duracion del Ataque"] = valorRK
            fila.at[0, "Estado Informes"] = servidorInformes.get_estado()
            fila.at[0, "Informes ocupado por"] = servidorInformes.get_siendoAtendido()
            fila.at[0, "Cola Informes"] = "Longitud: " +str(len(servidorInformes.get_cola())) +" "+ str([i.get_documento() for i in servidorInformes.get_cola()])
            fila.at[0, "Estado Reservas"] = servidorReservas.get_estado()
            fila.at[0, "Reservas ocupado por"] = servidorReservas.get_siendoAtendido()
            fila.at[0, "Cola Reservas"] = "Longitud: " +str(len(servidorReservas.get_cola())) +" "+ str([i.get_documento() for i in servidorReservas.get_cola()])
            fila.at[0, "Tiempo oscioso informes"] = servidorInformes.get_tiempoOscioso()
            fila.at[0, "Tiempo oscioso reservas"] = servidorReservas.get_tiempoOscioso()
            fila.at[0, "Porcentaje de trabajo de alarmas"] = tiempoDeTrabajoAlarma/reloj
            fila.at[0, "Atendidos en informes"] = servidorInformes.get_atendidos()
            fila.at[0, "Atendidos en reservas"] = servidorReservas.get_atendidos()
            fila.at[0, "Cantidad de personas esperando"] = len(servidorInformes.get_cola()) + len(servidorReservas.get_cola())
            fila.at[0, "Cantidad de personas atendidas"] = servidorReservas.get_atendidos() + servidorInformes.get_atendidos()




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





