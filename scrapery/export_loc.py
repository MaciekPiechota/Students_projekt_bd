from auchany import find_auchany
from zabki import *
from lokalizacja import *
import csv

def exprt():
    sklepy = find_zabki()

    with open('sklepy.csv', mode='w') as csv_file:
        fieldnames = ['name', 'lat', 'lng', 'nr', 'street', 'district', 'zip']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for s in sklepy:
            writer.writerow({'name': s.typ, 'lat': s.lat, 'lng': s.lng,
                            'nr': s.nr_domu, 'street': s.ulica, 'district' : s.dzielnica, 'zip' : s.kod_pocztowy})

exprt()