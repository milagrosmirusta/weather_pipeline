from dagster import Definitions, load_assets_from_modules, ScheduleDefinition,define_asset_job
from dagster_project.assets import ingestion, transformation, load
all_assets = load_assets_from_modules([ingestion, transformation, load])

weather_job = define_asset_job(
    name="weather_pipeline_job",
    selection="*"  
)

# Schedule para correr cada hora
weather_schedule = ScheduleDefinition(
    name="weather_hourly",
    job=weather_job,
    cron_schedule="0 * * * *",  
)

defs = Definitions(
    assets=all_assets,
    jobs=[weather_job],
    schedules=[weather_schedule],
)