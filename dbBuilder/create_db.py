import psycopg2
from csv import reader
import os


dsn = "host=localhost dbname=postgres user=postgres password=postgres"
conn = psycopg2.connect(dsn)

def create_shop_table():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE shop (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """)
    conn.commit()

def create_localization_table():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE localization (
            id_sklepu INTEGER NOT NULL REFERENCES shop,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            number VARCHAR(255) NOT NULL,
            street VARCHAR(255) NOT NULL,
            district VARCHAR(255) NOT NULL,
            postcode VARCHAR(255) NOT NULL
        )
        """)
    conn.commit()



def load_shops_data():

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO shop (name)
        VALUES ('Żabka'),
               ('Auchan'),
               ('Biedronka'),
              ('Carrefour');
          """)

    local_path = os.getcwd()
    shops_paths = []
    
    cur.execute("""SELECT s.id FROM shop s where s.name = 'Żabka' """)
    shops_paths.append([cur.fetchall()[0][0],local_path+"/shops/zabki.csv"])

    cur.execute("""SELECT s.id FROM shop s where s.name = 'Auchan' """)
    shops_paths.append([cur.fetchall()[0][0],local_path+"/shops/auchany.csv"])
    
    cur.execute("""SELECT s.id FROM shop s where s.name = 'Biedronka' """)
    shops_paths.append([cur.fetchall()[0][0],local_path+"/shops/biedronki.csv"])

    cur.execute("""SELECT s.id FROM shop s where s.name = 'Carrefour' """)
    shops_paths.append([cur.fetchall()[0][0],local_path+"/shops/carrefoury.csv"])

    for path in shops_paths:
        print(path[0],path[1])
        with open(path[1],'r') as csv_obj:
            csv_reader = reader(csv_obj)
            for row in csv_reader:
                cur.execute("""
                INSERT INTO localization(id_sklepu,latitude,longitude,number,street,district,postcode)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,(path[0],row[0],row[1],row[2],row[3],row[4],row[5]))
    conn.commit()

def create_product_table():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE product (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            type VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            price REAL NOT NULL,
            amount REAL NOT NULL,
            discount boolean NOT NULL
        )
        """)
    conn.commit()

def create_selling_table():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE selling (
            shop_id INTEGER NOT NULL REFERENCES shop,
            product_id INTEGER NOT NULL REFERENCES product,
            PRIMARY KEY (shop_id,product_id)
        )
    """)
    conn.commit()


def load_products_data():

    shop_names = ['Żabka','Auchan','Biedronka','Carrefour']
    name_id = {}
    cur = conn.cursor()

    for name in shop_names:
        cur.execute("""SELECT id 
                         FROM shop s 
                        WHERE s.name = %s
                    """,[name])
        name_id[name] = cur.fetchall()[0][0]

    print(name_id)

    local_path = os.getcwd()

    product_paths = []
    product_paths.append(local_path+"/products/ENERG.csv")
    product_paths.append(local_path+"/products/PIZZA.csv")
    product_paths.append(local_path+"/products/PIWO.csv")

    for path in product_paths:
        print(path)
        with open(path,'r') as csv_obj:
            csv_reader = reader(csv_obj)
            for row in csv_reader:
                cur.execute("""
                    INSERT INTO product (type,name,price,amount,discount)
                    VALUES (%s,%s,%s,%s,%s) RETURNING id
                """,(row[0],row[1],row[2],row[3],row[4]))
                product_id = cur.fetchone()[0]
                shop_id = name_id[row[5]]

                cur.execute("""
                INSERT INTO selling
                VALUES (%s,%s)
                """,(shop_id,product_id))
    
    conn.commit()

# https://www.mkompf.com/gps/distcalc.html
# zródło z wzorem na odległość
def create_distance_function():
    cur = conn.cursor()

    cur.execute("""
    CREATE OR REPLACE FUNCTION distance(a_lat real, a_log real, b_lat real, b_log real) RETURNS real AS $$
    DECLARE
    d real;
    BEGIN
    d := round(sqrt( (111000*(a_lat-b_lat))^2 + (111000*(a_log-b_log))^2 ));
    RETURN  d;
    END;
    $$ LANGUAGE plpgsql;  
    """)


#tworzenie tabel

#create_shop_table()
#create_localization_table()
#create_product_table()
#create_selling_table()
#load_shops_data()
#load_products_data()
#create_distance_function()

