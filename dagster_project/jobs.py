from dagster import job
from assets.ingestion import ingest_weather
from assets.transformation import transform_weather
from assets.load import load_to_dw
from assets.ingestion_forecast import ingest_forecast
from assets.transform_forecast import transform_forecast
from assets.load_forecast import load_to_dw_forecast

@job
def weather_job():
     load_to_dw(transform_weather(ingest_weather()))

@job
def forecast_job():
     load_to_dw_forecast(transform_forecast(ingest_forecast()))