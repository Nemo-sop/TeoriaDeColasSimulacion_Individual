class Evento:
    def __init__(self, tipo, tiempo, persona):
        self.__tipo = tipo
        self.__tiempo = tiempo
        self.__persona = persona

    def __lt__(self, other):
        return self.__tiempo < other.get_tiempo()
    def __gt__(self, other):
        return self.__tiempo > other.get_tiempo()

    def get_tiempo(self):
        return self.__tiempo

    def get_tipoEvento(self):
        return self.__tipo

    def get_persona(self):
        return self.__persona

    def add_tiempo(self, tiempoExtra):
        self.__tiempo += tiempoExtra

    def set_tiempo(self, tiempo):
        self.__tiempo = tiempo