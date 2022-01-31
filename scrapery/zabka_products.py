from tkinter import E
from product import *
import json

PIWO = [7, [], Type.PIWO]
ENERG = [1, ["energ", "kofei"], Type.ENERGY]


def is_unit(unit):
    return unit == 'ml' or unit == 'l' or unit == 'kg' or unit == 'g'


def get_amount(name):
    name_s = name.split(' ')

    i = len(name_s) - 1
    while i >= 0 and not is_unit(name_s[i]):
        i -= 1

    if i == -1:
        return 0.0

    unit = name_s[i]
    amount = name_s[i - 1]
    if name_s[i - 2] == 'x':
        return [float(amount) * float(name_s[i - 3]), unit]
    else:
        return [float(amount), unit]


def scrape_zabka(what):
    if what == "PIWO":
        type = PIWO
    elif what == "ENERG":
        type = ENERG
    else:
        return []

    with open('zabka_uber.json') as json_file:
        products = []

        data = json.load(json_file)["hasMenu"]["hasMenuSection"]
        data_products = data[type[0]]["hasMenuItem"]
        for p in data_products:
            desc = p["description"]
            if len(type[1]) > 0:
                ok = False
            else:
                ok = True

            for word in type[1]:
                if word in desc:
                    ok = True
                    break

            if ok:
                name = p["name"].strip().replace('WIELOSZTUKA ', '')
                price = float(p["offers"]["price"]) / 100
                discount = False
                amount_ = get_amount(name)
                amount = convert_unit(amount_[0], amount_[1])
                products.append(
                    Product(type[2], name, price, amount, discount))

        return products
