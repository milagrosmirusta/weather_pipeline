from dagster import (
    Definitions,
    load_assets_from_modules,
    ScheduleDefinition,
    define_asset_job
)

from dagster_project.assets import ingestion, transformation, load
from dagster_project.assets import ingestion_forecast, transform_forecast, load_forecast


all_assets = load_assets_from_modules([
    ingestion,
    transformation,
    load,
    ingestion_forecast,
    transform_forecast,
    load_forecast
])

# Job actual (current weather)
weather_job = define_asset_job(
    name="weather_pipeline_job",
    selection="*"  
)

weather_schedule = ScheduleDefinition(
    name="weather_hourly",
    job=weather_job,
    cron_schedule="0 * * * *",  
)

forecast_job = define_asset_job(
    name="forecast_pipeline_job",
    selection=[
        "load_to_dw_forecast"  # dispara ingest + transform + load forecast
    ],
)

forecast_schedule = ScheduleDefinition(
    name="forecast_daily",
    job=forecast_job,
    cron_schedule="0 8 * * *",  
)

defs = Definitions(
    assets=all_assets,
    jobs=[weather_job, forecast_job],
    schedules=[weather_schedule, forecast_schedule],
)
