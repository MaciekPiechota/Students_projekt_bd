from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import requests
from lokalizacja import *

URL = "https://www.carrefour.pl/sklepy?page="

dzielnice = ['Wawer', 'Wola', 'Śródmieście', 'Bemowo', 'Bielany', 'Ursynów',
             'Żoliborz', 'Włochy', 'Praga-Północ', 'Praga-Południe', 'Mokotów', 'Wilanów', 'Ochota', 'Targówek', 'Białołęka', 'Ursus', 'Rembertów', 'Wesoła']

def find_carrefoury():
    geolocator = Nominatim(user_agent='Students')
    carrefoury = []
    count = 0
    for i in range(78):
        r = requests.get(URL + str(i)).text
        soup = BeautifulSoup(r, 'html.parser')
        elements = soup.find_all('div', class_='jss262 jss263')
        print(count)
        for element in elements:
            count += 1
            print(count)

            adr = element.find('p', class_='MuiTypography-root MuiTypography-body1').text.replace('.', ' ').split(' ')
            if adr[-1] != 'Warszawa':
                continue
            adr = adr[2:-1]
            zip = adr[-1][-6:]
            nr_ulicy = adr[-1][:-6]
            adr = adr[:-1]
            if len(adr) > 3 and adr[-1] == '':
                nr_ulicy = adr[-3]
                adr = adr[:-3]
            elif adr[-1] == 'lok' or adr[-1] == 'lokal':
                nr_ulicy = adr[-2]
                adr = adr[:-2]


            ok = True
            for el in adr:
                if el.isnumeric():
                    ok = False
                    break

            if not ok:
                continue

            ulica = ' '.join(adr).replace('  ', '. ')
            location = geolocator.geocode(zip)
            dzielnica = 'Wola'
            for d in dzielnice:
                if d in location.address:
                    dzielnica = d
                    break
            data = [nr_ulicy, ulica, dzielnica, '', '', zip]
            print(data)
            carrefoury.append(Lokalizacja(location.latitude, location.longitude, data, "Carrefour"))

    return carrefoury
