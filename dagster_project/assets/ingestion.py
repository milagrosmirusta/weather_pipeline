from dagster import asset
import pandas as pd
from datetime import datetime
import os
from dagster_project.resources import WeatherAPIClient

@asset
def ingest_weather() -> pd.DataFrame:
    """
    Ingesta datos del clima desde OpenWeather API para múltiples ciudades argentinas
    """
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
    
    client = WeatherAPIClient()
    raw_data = client.get_multiple_cities(cities)
    
    # DF
    records = []
    for data in raw_data:
        record = {
            'city': data['name'],
            'country': data['sys']['country'],
            'latitude': data['coord']['lat'],      
            'longitude': data['coord']['lon'],     
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind'].get('deg', None),  
            'pressure': data['main']['pressure'],   
            'visibility': data.get('visibility', None),  
            'condition_id': data['weather'][0]['id'],
            'condition_main': data['weather'][0]['main'],
            'condition_description': data['weather'][0]['description'],
            'timestamp': datetime.now(),
            'api_timestamp': datetime.fromtimestamp(data['dt'])
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    
    # Guardar en raw 
    os.makedirs('data/raw', exist_ok=True)
    filepath = f"data/raw/weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    df.to_parquet(filepath)
    
    print(f"Ingesta completada: {len(df)} registros guardados en {filepath}")
    
    return df