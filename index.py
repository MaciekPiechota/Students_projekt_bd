from flask import Flask, render_template, request
import psycopg2
from geopy.geocoders import Nominatim

app = Flask(__name__)
dsn = "host=localhost dbname=postgres user=postgres password=postgres"
conn = psycopg2.connect(dsn)
geolocator = Nominatim(user_agent='Maciek')
epsilon = 0.0000006;


@app.route("/")
def index():
    return render_template('index.html')
  
def closest_shop_query(cur,lat,log,epsilon,num_of_rows):
  cur.execute("""
  SELECT s.name, l.street, l."number",
    CASE WHEN (l.latitude - %s)^2 + (l.longitude-%s)^2 < %s then 0
    ELSE (2*6371*asin(sqrt( (sin((l.latitude -%s)/2))^2 + cos(%s)*cos(l.latitude)*(sin((l.longitude - %s)/2))^2)))
     END AS distance, round(sqrt((111000*(l.latitude - %s))^2+(111000*(l.longitude - %s))^2))
    FROM shop s 
    JOIN localization l 
      ON s.id = l.id_sklepu 
   ORDER BY distance
   limit %s
  """,(lat,log,epsilon,lat,lat,log,lat,log,num_of_rows))
  return cur.fetchall()

@app.route('/', methods=['POST'])
def my_form_post():
    if request.form.get("query1"):
        district = request.form['district']
        num_of_rows = int(request.form['num_of_records'])
        address = request.form['address']

        location = geolocator.geocode(address)
        lat = location.latitude
        log = location.longitude

        cur = conn.cursor()

        cur.execute("""
            SELECT s.name, l.street, l."number",round(sqrt((111000*(l.latitude - %s))^2+(111000*(l.longitude - %s))^2)) as d
              FROM shop s join localization l 
                ON s.id = l.id_sklepu AND l.district = %s
                ORDER BY d
                limit %s
         """,(lat,log,district,num_of_rows))

        rows = cur.fetchall()
        print(rows)
        cur.close()

        return render_template('query_1_template.html',rows=rows,title="Sklepy na dzielnicy "+district)
    elif request.form.get("query2"):
        address = request.form['address']
        num_of_rows = int(request.form['num_of_records'])

        location = geolocator.geocode(address)
        lat = location.latitude
        log = location.longitude
        cur = conn.cursor()

        rows = closest_shop_query(cur,lat,log,epsilon,num_of_rows)

        return render_template('query_2_template.html',rows=rows,title="Sklepy najbliżej ciebie")
    elif request.form.get("query3"):
      category = request.form['category']
      num_of_rows = int(request.form['num_of_records'])
      address = request.form['address']
      cur = conn.cursor()

      if address == '':
        cur.execute("""
        SELECT p.name as nazwa, p.price as cena, p.amount as ml 
          FROM product p
          WHERE p."type" = %s
        ORDER BY cena
        limit %s
          """,(category,num_of_rows))
      else:

        location = geolocator.geocode(address)
        lat = location.latitude
        log = location.longitude

        closest_shop_name = closest_shop_query(cur,lat,log,epsilon,1)[0][0]

        cur.execute("""
          SELECT s.id 
            FROM shop s 
           WHERE s.name = %s
           """,[closest_shop_name])        

        closest_shop_id = cur.fetchall()[0][0]
        print(closest_shop_id,category)

        cur.execute("""
        SELECT DISTINCT p.name , p.price as cena, p.amount
          FROM product p 
          JOIN selling s 
            ON s.shop_id = %s and s.product_id = p.id
          WHERE p."type" = %s
        ORDER BY cena
        limit %s
          """,(closest_shop_id,category,num_of_rows))


      rows = cur.fetchall()
      cur.close()

      return render_template('query_3_template.html',rows=rows,title="Najtasze produkty z kategori "+category)
    elif request.form.get("query4"):

      product = request.form['product']
      product_sql = "%" + request.form['product'] + "%"
      address = request.form['address']
      location = geolocator.geocode(address)
      lat = location.latitude
      log = location.longitude

      cur = conn.cursor()

      cur.execute("""
      SELECT s.name, l.street, l.number, p.name, p.price, round(sqrt((111000*(l.latitude - %s))^2+(111000*(l.longitude - %s))^2))
        FROM shop s
        JOIN localization l
          ON s.id = l.id_sklepu AND (111000*(l.latitude - %s))^2+(111000*(l.longitude - %s))^2 < 500^2
        JOIN selling s1
          ON s1.shop_id = l.id_sklepu
        JOIN product p
          ON s1.product_id = p.id
       WHERE p.name like %s
      """,(lat,log,lat,log,product_sql))

      rows = cur.fetchall()

      return render_template('query_4_template.html',rows=rows,title=product+" blisko ciebie")
