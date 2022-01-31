from product import *
from bs4 import BeautifulSoup
import requests

URL = 'https://www.carrefour.pl/'
ENERG_URL = URL + 'napoje/napoje-gazowane-i-niegazowane/energetyki'
PIZZA_URL = URL + 'mrozonki/pizza-9s'

PIZZA_NO = '290'
ENERG_NO = '287'

PIZZA_PAGES_NO = '442'
ENERG_PAGES_NO = '551'

DISCOUNT_CLASS = ' MuiTypography-colorError'

PIZZA_PRICE_CLASS = 'MuiTypography-root jss208 jss295 MuiTypography-h3'
ENERG_PRICE_CLASS = 'MuiTypography-root jss208 jss292 MuiTypography-h3'

PIZZA_NAME_CLASS = 'MuiButtonBase-root jss306'
ENERG_NAME_CLASS = 'MuiButtonBase-root jss303'

AMOUNT_CLASS = 'MuiTypography-root MuiTypography-body1 MuiTypography-colorTextSecondary'

PIZZA = [PIZZA_URL, PIZZA_NO, PIZZA_NAME_CLASS,
         PIZZA_PRICE_CLASS, PIZZA_PRICE_CLASS + DISCOUNT_CLASS, AMOUNT_CLASS, Type.PIZZA, PIZZA_PAGES_NO]

ENERG = [ENERG_URL, ENERG_NO, ENERG_NAME_CLASS,
         ENERG_PRICE_CLASS, ENERG_PRICE_CLASS + DISCOUNT_CLASS, AMOUNT_CLASS, Type.ENERGY, ENERG_PAGES_NO]


def scrape_crfr(what):
    if what == "PIZZA":
        t = PIZZA
    elif what == "ENERG":
        t = ENERG
    else:
        return []

    soup = BeautifulSoup(requests.get(t[0]).text, 'html.parser')

    pages = soup.find_all('div', class_='jss' + t[7])
    no_pages = int(pages[0].find(
        'p', class_='MuiTypography-root MuiTypography-body1').text.split(' ')[-1])

    products = []

    for i in range(0, no_pages):
        if (i > 0):
            soup = BeautifulSoup(requests.get(
                t[0] + '?page=' + str(i)).text, 'html.parser')

        elements = soup.find_all('div', class_='jss' + t[1])

        for element in elements:
            name = element.find('a', class_=t[2]).text
            price = element.find('div', class_=t[3])
            discount = False
            if price is None:
                price = element.find(
                    'div', class_=t[4])
                discount = True

            price_num = float(price.text[:-3].replace(',', '.'))
            amount = element.find('p', class_=t[5]).text.split(' ')
            amount_num = convert_unit(
                float(amount[0].replace(',', '.')), amount[1])
            products.append(Product(t[6],
                                    name, price_num, amount_num, discount))

    return products
