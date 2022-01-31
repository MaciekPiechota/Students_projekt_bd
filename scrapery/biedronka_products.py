from carrefour_products import AMOUNT_CLASS
from product import *
import requests

ENERG_URL = "https://api.glovoapp.com/v3/stores/131416/addresses/236396/content?nodeType=DEEP_LINK&link=napoje-sc.96190474%2Fnapoje-energetyczne-c.512596257"
PIZZA1_URL = "https://api.glovoapp.com/v3/stores/131416/addresses/236396/content?nodeType=DEEP_LINK&link=szybkie-dania-sc.96190483%2Fwloskie-c.512596260"
PIZZA2_URL = "https://api.glovoapp.com/v3/stores/131416/addresses/236396/content?nodeType=DEEP_LINK&link=szybkie-dania-sc.96190483%2Fdania-mrozone-c.512596256"

ENERG = [[ENERG_URL, 0, Type.ENERGY]]
PIZZA1 = [PIZZA1_URL, 0, Type.PIZZA]
PIZZA2 = [PIZZA2_URL, 1, Type.PIZZA]
PIZZA = [PIZZA1, PIZZA2]


def is_unit(unit):
    return unit == 'ml' or unit == 'l' or unit == 'kg' or unit == 'g'


def get_amount(name):
    name = name.replace(':', '')

    if '500ml' in name or '0,5l' in name:
        return [0.5, 'l']
    if '250ml' in name or '0,25l' in name:
        return [0.25, 'l']

    name_s = name.replace(':', '').split(' ')

    i = len(name_s) - 1
    while i >= 0 and not is_unit(name_s[i]):
        i -= 1

    if i == -1:
        return [0.0, 'l']

    unit = name_s[i]
    amount = name_s[i - 1].split('x')
    if len(amount) == 2:
        if not amount[0].isnumeric():
            return [0.0, 'l']
        return [float(amount[0]) * float(amount[1]), unit]
    else:
        return [float(amount[0].replace(',', '.')), unit]


def scrape_biedronka(what):
    if what == "PIZZA":
        type_ = PIZZA
    elif what == "ENERG":
        type_ = ENERG
    else:
        return []

    products = []

    for type in type_:
        r = requests.get(type[0], headers={
            "accept": "application/json",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "glovo-api-version": "14",
            "glovo-app-development-state": "Production",
            "glovo-app-platform": "web",
            "glovo-app-type": "customer",
            "glovo-app-version": "7",
            "glovo-delivery-location-accuracy": "0",
            "glovo-delivery-location-latitude": "52.2451247",
            "glovo-delivery-location-longitude": "20.9909262",
            "glovo-delivery-location-timestamp": "1643112016925",
            "glovo-device-id": "791662350",
            "glovo-language-code": "pl",
            "glovo-location-city-code": "WAW",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-datadog-origin": "rum",
            "x-datadog-parent-id": "6887431878334299423",
            "x-datadog-sampled": "1",
            "x-datadog-sampling-priority": "1",
            "x-datadog-trace-id": "5058555860902138406"
        })
        products_data = r.json()["data"]["body"][type[1]]["data"]["elements"]

        for p in products_data:
            p_data = p["data"]
            name = p_data["name"]
            price = p_data["price"]
            discount = False
            amount_ = get_amount(name)
            amount = convert_unit(amount_[0], amount_[1])
            products.append(Product(type[2], name, price, amount, discount))

    return products
