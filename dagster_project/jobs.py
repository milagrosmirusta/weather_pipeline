from dagster import job
from assets.ingestion import ingest_weather
from assets.transform import transform_weather
from assets.load import load_to_dw

@job
def weather_job():
    load_to_dw(transform_weather(ingest_weather()))
