from geopy.geocoders import Nominatim
import json

from lokalizacja import Lokalizacja

dzielnice = ['Wawer', 'Wola', 'Śródmieście', 'Bemowo', 'Bielany', 'Ursynów',
             'Żoliborz', 'Włochy', 'Praga-Północ', 'Praga-Południe', 'Mokotów', 'Wilanów', 'Ochota', 'Targówek', 'Białołęka', 'Ursus', 'Rembertów', 'Wesoła']

def find_auchany():
    geolocator = Nominatim(user_agent="Student\'s")
    auchany = []
    with open("auchan.json") as json_file:
        data = json.load(json_file)
        for loc in data:
            loc_data = loc['address']
            if loc_data['city'] != 'Warszawa':
                continue

            lat = loc_data['latitude']
            lng = loc_data['longitude']

            location = geolocator.reverse([lat, lng])
            loc_data = location.address.split(", ")
            if not loc_data[0].isnumeric() and loc_data[1][0].isnumeric():
                loc_data = loc_data[1:]

            i = 2
            while loc_data[i] not in dzielnice:
                i += 1

            loc_data = loc_data[:2] + loc_data[i:]

            auchany.append(Lokalizacja(lat, lng, loc_data, "Auchan"))
        
    return auchany

find_auchany()