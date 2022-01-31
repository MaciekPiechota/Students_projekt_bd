from enum import Enum


class Type(Enum):
    ENERGY = 1
    PIZZA = 2
    PIWO = 3


def convert_unit(amount, unit):
    if (unit == 'g'):
        return amount / 1000
    if (unit == 'ml'):
        return amount / 1000
    else:
        return amount


def simp_name(name):
    return name.replace(',', '')


class Product:
    def __init__(self, type, name, price, amount, discount):
        if type == Type.ENERGY:
            self.type = 'ENERGETYK'
        elif type == Type.PIWO:
            self.type = 'PIWO'
        else:
            self.type = 'PIZZA'

        self.name = simp_name(name)
        self.price = price
        self.amount = amount
        self.discount = discount

    def print(self):
        print(self.name)
        print(self.amount)
        print(self.price)
        print(self.discount)
        print()
