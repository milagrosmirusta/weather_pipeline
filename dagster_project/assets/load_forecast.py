from dagster import asset
import pandas as pd
from dagster_project.resources import DatabaseClient
from sqlalchemy import text

@asset
def load_to_dw_forecast(transform_forecast):
    fact_forecast = transform_forecast
    
    db_client = DatabaseClient()
    engine = db_client.get_engine()

    dim_conditions = transform_forecast[[
        "condition_id", "main", "description"
    ]].drop_duplicates()

    # 2. Traer conditions existentes
    existing_conditions = pd.read_sql(
        "SELECT condition_id FROM dim_conditions",
        engine
    )

    # 3. Filtrar nuevas
    new_conditions = dim_conditions[
        ~dim_conditions["condition_id"].isin(existing_conditions["condition_id"])
    ]

    # 4. Insertar nuevas conditions con datos reales
    if len(new_conditions) > 0:
        new_conditions.to_sql(
            "dim_conditions",
            engine,
            if_exists="append",
            index=False,
            method="multi"
        )
        print(f"Dim_conditions: agregadas {len(new_conditions)} nuevas.")
    else:
        print("Dim_conditions: no hay nuevas condiciones.")


    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_forecast"))

    # Mapear city_id
    city_mapping = pd.read_sql(
        'SELECT city_id, city_name FROM dim_city',
        engine
    )

    fact_ids = fact_forecast.merge(city_mapping, on="city_name", how="left")

    fact_final = fact_ids[[
        "city_id", "timestamp", "temp", "feels_like", "humidity",
        "wind_speed", "wind_deg", "pressure", "visibility",
        "condition_id", "ingestion_timestamp"
    ]]

    # Insert
    fact_final.to_sql(
        "fact_forecast",
        engine,
        index=False,
        if_exists="append",
        method="multi"
    )

    print(f"Cargados {len(fact_final)} registros de forecast (tabla reemplazada)")
