from dagster import asset
import pandas as pd

@asset
def transform_forecast(ingest_forecast: pd.DataFrame) -> pd.DataFrame:
    df = ingest_forecast.copy()

    fact_forecast = df[[
        "city_name", "forecast_timestamp", "temp", "feels_like",
        "humidity", "wind_speed", "wind_deg", "pressure", "visibility",
        "condition_id", "ingestion_timestamp", "condition_main", "condition_description"
    ]].copy()

    fact_forecast.columns = [
        "city_name", "timestamp", "temp", "feels_like",
        "humidity", "wind_speed", "wind_deg", "pressure",
        "visibility", "condition_id", "ingestion_timestamp", "main", "description"
    ]

    print(f"Transformación Forecast completada: {len(fact_forecast)} registros")

    return fact_forecast
