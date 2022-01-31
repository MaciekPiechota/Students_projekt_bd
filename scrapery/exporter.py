import csv
from product import *
from auchan_products import *
from carrefour_products import *
from zabka_products import *
from biedronka_products import *


def exprt(type):
    products = scrape_auchan(type)
    products.extend(scrape_biedronka(type))
    products.extend(scrape_zabka(type))
    products.extend(scrape_biedronka(type))

    with open(type + '.csv', mode='w') as csv_file:
        fieldnames = ['type', 'name', 'price', 'amount', 'discount']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for p in products:
            writer.writerow({'type': p.type, 'name': p.name, 'price': p.price,
                            'amount': p.amount, 'discount': p.discount})


exprt("PIWO")
exprt("ENERG")
exprt("PIZZA")
