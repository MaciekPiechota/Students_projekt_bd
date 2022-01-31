from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import requests
from lokalizacja import *

URL = "https://www.biedronka.pl/pl/sklepy/lista,city,warszawa,page,"

dzielnice = ['Wawer', 'Wola', 'Śródmieście', 'Bemowo', 'Bielany', 'Ursynów',
             'Żoliborz', 'Włochy', 'Praga-Północ', 'Praga-Południe', 'Mokotów', 'Wilanów', 'Ochota', 'Targówek', 'Białołęka', 'Ursus', 'Rembertów', 'Wesoła']

def find_biedronki():
    geolocator = Nominatim(user_agent='Students')
    biedronki = []
    for i in range(1, 10):
        r = requests.get(URL + str(i)).text
        soup = BeautifulSoup(r, 'html.parser')
        shops = soup.find_all('span', class_='shopAddress')
        for s in shops:
            addr = s.text.strip().split("\r")
            zip = addr[0]
            addr[1] = addr[1].strip()
            # dla jednego przypadku
            if addr[1][-1] == '.':
                addr[1] = addr[1][:-6]

            ulica_split = addr[1].split(' ')
            nr_ulicy = ulica_split[-1]
            ulica = ' '.join(ulica_split[:-1])
            location = geolocator.geocode(zip)
            dzielnica = 'Wola'
            for d in dzielnice:
                if d in location.address:
                    dzielnica = d
                    break
            data = [nr_ulicy, ulica, dzielnica, '', '', zip]
            biedronki.append(Lokalizacja(location.latitude, location.longitude, data, "Biedronka"))
    return biedronki
            


find_biedronki()
