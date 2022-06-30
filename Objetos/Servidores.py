
class Servidor:
    def __init__(self, sector, estado, cola, tiempoOscioso, atendidos):
        self.__sector = sector
        self.__estado = estado
        self.__cola = cola
        self.__seDesocupo = 0
        self.__tiempoOscioso = tiempoOscioso
        self.__atendidos = atendidos
        self.__siendoAtendido = None

    def mover_cola(self):
        self.__cola.pop(0)

    def get_siendoAtendido(self):
        return self.__siendoAtendido

    def set_siendoAtendido(self, persona):
        self.__siendoAtendido = persona

    def add_tiempoOscioso(self, tiempo):
        self.__tiempoOscioso += tiempo

    def get_seDesocupo(self):
        return self.__seDesocupo

    def set_seDesocupo(self, momento):
        self.__seDesocupo = momento

    def reiniciar_seDesocupo(self):
        self.__seDesocupo = 0

    def get_atendidos(self):
        return self.__atendidos

    def agregarAtendido(self):
        self.__atendidos += 1

    def get_estado(self):
        return self.__estado

    def set_estado(self, estado):
        self.__estado = estado

    def get_cola(self):
        return self.__cola

    def add_cola(self, persona):
        self.__cola.append(persona)

    def get_elQueSigue(self):
        return self.__cola[0]
