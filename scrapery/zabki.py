from geopy.geocoders import Nominatim
import json

from lokalizacja import Lokalizacja

dzielnice = ['Wawer', 'Wola', 'Śródmieście', 'Bemowo', 'Bielany', 'Ursynów',
             'Żoliborz', 'Włochy', 'Praga-Północ', 'Praga-Południe', 'Mokotów', 'Wilanów', 'Ochota', 'Targówek', 'Białołęka', 'Ursus', 'Rembertów', 'Wesoła']


def find_zabki():
    geolocator = Nominatim(user_agent="Student\'s")
    zabki = []
    with open("zabki.json") as json_file:
        data = json.load(json_file)
        for loc in data:
            if loc["lat"] > 52.38 or loc["lat"] < 52.07 or loc["lng"] < 20.82 or loc["lng"] > 21.28:
                continue
            location = geolocator.reverse(
                str(loc["lat"]) + ", " + str(loc["lng"]))
            loc_data = location.address.split(", ")
            if 'Warszawa' not in loc_data:
                continue
            if not loc_data[0].isnumeric() and loc_data[1][0].isnumeric():
                loc_data = loc_data[1:]
            elif loc_data[0] == "Żabka":
                loc_data = ['1'] + loc_data[1:]

            if not loc_data[0][0].isnumeric():
                continue

            i = 2
            while loc_data[i] not in dzielnice:
                i += 1

            loc_data = loc_data[:2] + loc_data[i:]

            zabki.append(Lokalizacja(loc["lat"], loc["lng"], loc_data, "Żabka"))
        
    return zabki
