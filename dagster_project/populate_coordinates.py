# sql/populate_coordinates.py
import psycopg2
from dotenv import load_dotenv
import os
from resources import WeatherAPIClient

load_dotenv()

# Conectar a DB
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

# Obtener ciudades sin coordenadas
cur.execute("SELECT city_id, city_name, country FROM dim_city WHERE latitude IS NULL")
cities_to_update = cur.fetchall()

print(f"Actualizando coordenadas para {len(cities_to_update)} ciudades...")

# API client
api_client = WeatherAPIClient()

for city_id, city_name, country in cities_to_update:
    try:
        # Consultar API
        data = api_client.get_weather(f"{city_name},{country}")
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        
        # Actualizar en DB
        cur.execute(
            "UPDATE dim_city SET latitude = %s, longitude = %s WHERE city_id = %s",
            (lat, lon, city_id)
        )
        print(f" {city_name}: ({lat}, {lon})")
        
    except Exception as e:
        print(f"   Error con {city_name}: {e}")

conn.commit()
cur.close()
conn.close()

print("\nMigración completada!")