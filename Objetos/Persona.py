import random


class Persona:
    def __init__(self):
        self.__documento = random.randint(100000, 999999)

    def anular(self):
        self.__documento = 0

