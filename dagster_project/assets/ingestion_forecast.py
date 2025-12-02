from dagster import asset
import pandas as pd
from datetime import datetime
import os
from dagster_project.resources import WeatherAPIClient

@asset
def ingest_forecast() -> pd.DataFrame:

    cities = [
        "Buenos Aires,AR", "Catamarca,AR", "Córdoba,AR", "Corrientes,AR",
        "Formosa,AR", "La Plata,AR", "La Rioja,AR", "Mendoza,AR",
        "Neuquén,AR", "Paraná,AR", "Posadas,AR", "Rawson,AR",
        "Resistencia,AR", "Río Gallegos,AR", "Salta,AR", "San Juan,AR",
        "San Luis,AR", "San Miguel de Tucumán,AR", "San Salvador de Jujuy,AR",
        "Santa Fe,AR", "Santa Rosa,AR", "Santiago del Estero,AR",
        "Ushuaia,AR", "Viedma,AR", "Rosario,AR", "Mar del Plata,AR",
        "Rio Cuarto,AR"
    ]

    client = WeatherAPIClient()
    records = []

    for city in cities:
        try:
            data = client.get_forecast(city)
            city_name = data["city"]["name"]
            country = data["city"]["country"]
            lat = data["city"]["coord"]["lat"]
            lon = data["city"]["coord"]["lon"]

            for entry in data["list"]:
                record = {
                    "city_name": city_name,
                    "country": country,
                    "latitude": lat,
                    "longitude": lon,
                    "forecast_timestamp": entry["dt_txt"],
                    "temp": entry["main"]["temp"],
                    "feels_like": entry["main"]["feels_like"],
                    "humidity": entry["main"]["humidity"],
                    "pressure": entry["main"]["pressure"],
                    "wind_speed": entry["wind"]["speed"],
                    "wind_deg": entry["wind"].get("deg", None),
                    "visibility": entry.get("visibility", None),
                    "condition_id": entry["weather"][0]["id"],
                    "ingestion_timestamp": datetime.now(),
                    "condition_main": entry["weather"][0]["main"],
                    "condition_description": entry["weather"][0]["description"]
                }
                records.append(record)

        except Exception as e:
            print(f"Error obteniendo forecast para {city}: {e}")

    df = pd.DataFrame(records)

    os.makedirs("data/raw", exist_ok=True)
    filepath = f"data/raw/forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    df.to_parquet(filepath)

    print(f"Ingesta forecast completada ({len(df)} registros). Guardado en: {filepath}")

    return df
