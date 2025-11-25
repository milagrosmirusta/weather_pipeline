import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cur = conn.cursor()

# Contar registros en cada tabla
print("\n Datos en el Data Warehouse:")
print("="*40)

cur.execute("SELECT COUNT(*) FROM dim_conditions")
print(f"dim_conditions: {cur.fetchone()[0]} registros")

cur.execute("SELECT COUNT(*) FROM dim_city")
print(f"dim_city: {cur.fetchone()[0]} registros")

cur.execute("SELECT COUNT(*) FROM fact_weather")
print(f"fact_weather: {cur.fetchone()[0]} registros")

print("\n Últimos 5 registros de clima:")
print("="*40)

cur.execute("""
    SELECT 
        c.city_name,
        f.date,
        f.temp,
        f.humidity,
        cond.main as condition
    FROM fact_weather f
    JOIN dim_city c ON f.city_id = c.city_id
    JOIN dim_conditions cond ON f.condition_id = cond.condition_id
    ORDER BY f.date DESC
    LIMIT 5
""")

for row in cur.fetchall():
    print(f"{row[0]:15} | {row[1]} | {row[2]}°C | {row[3]}% | {row[4]}")

cur.close()
conn.close()