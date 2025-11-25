from dagster import asset
import pandas as pd

@asset
def transform_weather(ingest_weather: pd.DataFrame) -> dict:
    """
    Transforma los datos crudos en formato para el modelo estrella
    """
    df = ingest_weather.copy()
    
    # 1. Crear dim_conditions
    dim_conditions = df[['condition_id', 'condition_main', 'condition_description']].drop_duplicates()
    dim_conditions.columns = ['condition_id', 'main', 'description']
    
    # 2. Crear dim_city con coordenadas
    dim_city = df[['city', 'country', 'latitude', 'longitude']].drop_duplicates()
    dim_city.columns = ['city_name', 'country', 'latitude', 'longitude']
    dim_city = dim_city.reset_index(drop=True)
    
    # 3. Crear fact_weather
    fact_weather = df[[
        'city', 'api_timestamp', 'temp', 'feels_like', 
        'humidity', 'wind_speed', 'wind_deg', 'pressure', 
        'visibility', 'condition_id'
    ]].copy()
    fact_weather.columns = [
        'city_name', 'date', 'temp', 'feels_like',
        'humidity', 'wind_speed', 'wind_deg', 'pressure',
        'visibility', 'condition_id'
    ]
    
    print(f"Transformación completada:")
    print(f"   - {len(dim_conditions)} condiciones únicas")
    print(f"   - {len(dim_city)} ciudades")
    print(f"   - {len(fact_weather)} registros de hechos")
    
    return {
        'dim_conditions': dim_conditions,
        'dim_city': dim_city,
        'fact_weather': fact_weather
    }