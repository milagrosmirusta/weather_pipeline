import pandas as pd
from datetime import datetime, timedelta
import random
from resources import WeatherAPIClient, DatabaseClient

def generate_historical_data(days_back=60, cities=None):
    """
    Genera datos históricos de clima para los últimos N días
    
    Args:
        days_back: Cuántos días hacia atrás generar
        cities: Lista de ciudades (si es None, usa las default)
    """
    
    if cities is None:
        cities = [
        "Buenos Aires,AR",
        "Catamarca,AR",
        "Córdoba,AR",
        "Corrientes,AR",
        "Formosa,AR",
        "La Plata,AR",
        "La Rioja,AR",
        "Mendoza,AR",
        "Neuquén,AR",
        "Paraná,AR",
        "Posadas,AR",
        "Rawson,AR",
        "Resistencia,AR",
        "Río Gallegos,AR",
        "Salta,AR",
        "San Juan,AR",
        "San Luis,AR",
        "San Miguel de Tucumán,AR",
        "San Salvador de Jujuy,AR",
        "Santa Fe,AR",
        "Santa Rosa,AR",
        "Santiago del Estero,AR",
        "Ushuaia,AR",
        "Viedma,AR",
        "Rosario,AR",
        "Mar del Plata,AR",
        "Rio Cuarto, AR"
    ]
    
    # Cliente API
    api_client = WeatherAPIClient()
    db_client = DatabaseClient()
    engine = db_client.get_engine()
    
    print(f"Generando datos históricos para {days_back} días...")
    print(f"Ciudades: {len(cities)}")
    
    for day_offset in range(days_back, 0, -1):
        
        # Calcular la fecha simulada
        simulated_date = datetime.now() - timedelta(days=day_offset)
        
        raw_data = api_client.get_multiple_cities(cities)
        
        # Convertir a registros
        records = []
        for data in raw_data:
            
            # Agregar variación random para simular cambios históricos
            temp_variation = random.uniform(-5, 5)
            humidity_variation = random.randint(-15, 15)
            
            record = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'] + temp_variation,
                'feels_like': data['main']['feels_like'] + temp_variation,
                'humidity': max(0, min(100, data['main']['humidity'] + humidity_variation)),
                'wind_speed': data['wind']['speed'] + random.uniform(-2, 2),
                'condition_id': data['weather'][0]['id'],
                'condition_main': data['weather'][0]['main'],
                'condition_description': data['weather'][0]['description'],
                'timestamp': simulated_date,
                'api_timestamp': simulated_date
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        
        # === TRANSFORMACIÓN ===
        
        # dim_conditions
        dim_conditions = df[['condition_id', 'condition_main', 'condition_description']].drop_duplicates()
        dim_conditions.columns = ['condition_id', 'main', 'description']
        
        # Cargar conditions (ignora duplicados)
        try:
            dim_conditions.to_sql('dim_conditions', engine, if_exists='append', index=False, method='multi')
        except:
            pass  # Ya existen, no problem
        
        # dim_city
        dim_city = df[['city', 'country']].drop_duplicates()
        dim_city.columns = ['city_name', 'country']
        
        # Cargar solo ciudades nuevas
        existing_cities = pd.read_sql('SELECT city_name FROM dim_city', engine)
        new_cities = dim_city[~dim_city['city_name'].isin(existing_cities['city_name'])]
        
        if len(new_cities) > 0:
            new_cities.to_sql('dim_city', engine, if_exists='append', index=False, method='multi')
        
        # fact_weather
        fact_weather = df[['city', 'api_timestamp', 'temp', 'feels_like', 'humidity', 'wind_speed', 'condition_id']].copy()
        fact_weather.columns = ['city_name', 'date', 'temp', 'feels_like', 'humidity', 'wind_speed', 'condition_id']
        
        # Obtener city_id
        city_mapping = pd.read_sql('SELECT city_id, city_name FROM dim_city', engine)
        fact_weather_with_ids = fact_weather.merge(city_mapping, on='city_name', how='left')
        
        fact_final = fact_weather_with_ids[['city_id', 'condition_id', 'date', 'temp', 'feels_like', 'humidity', 'wind_speed']]
        
        # Insertar
        fact_final.to_sql('fact_weather', engine, if_exists='append', index=False, method='multi')
        
        print(f"  {simulated_date.strftime('%Y-%m-%d')}: {len(fact_final)} registros")
    
    # Resumen final
    total_records = pd.read_sql('SELECT COUNT(*) as count FROM fact_weather', engine)
    print(f"\nBackfill completado!")
    print(f"Total de registros en fact_weather: {total_records['count'][0]}")

if __name__ == "__main__":
    # Generar 30 días de historia
    generate_historical_data(days_back=30)