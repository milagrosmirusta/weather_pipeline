from dagster import asset
import pandas as pd
from dagster_project.resources import DatabaseClient

@asset
def load_to_dw(transform_weather):
    dim_conditions = transform_weather['dim_conditions']
    dim_city = transform_weather['dim_city']
    fact_weather = transform_weather['fact_weather']
    
    db_client = DatabaseClient()
    engine = db_client.get_engine()

    #1. Dim Conditions
    existing_conditions = pd.read_sql('SELECT condition_id FROM dim_conditions', engine)
    new_conditions = dim_conditions[~dim_conditions['condition_id'].isin(existing_conditions['condition_id'])]

    if len(new_conditions) > 0:
        new_conditions.to_sql(
            'dim_conditions',
            engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        print(f"Cargadas {len(new_conditions)} condiciones nuevas")
    else:
        print(f"No hay condiciones nuevas para cargar")


    #2. Dim Cities
    existing_cities = pd.read_sql('SELECT distinct city_name FROM dim_city', engine)
    new_cities = dim_city[~dim_city['city_name'].isin(existing_cities['city_name'])]
    if len(new_cities) > 0:
        new_cities.to_sql(
            'dim_city',
            engine,
            if_exists='append',
            index=False, method='multi'
        )
        print(f"Cargadas {len(new_cities)} ciudades nuevas")
    else:
        print(f"No hay ciudades nuevas para cargar")

    #3. Fact Weather
    city_mapping = pd.read_sql('SELECT city_id, city_name FROM dim_city', engine)
    fact_weather_ids=fact_weather.merge(city_mapping, how='left', on='city_name')
    fact_final = fact_weather_ids[['city_id', 'condition_id', 'date', 'temp', 
        'feels_like', 'humidity', 'wind_speed', 'wind_deg', 'pressure', 'visibility']]
    fact_final.to_sql('fact_weather', engine, index=False, if_exists='append',method='multi')

    print(f"Cargados {len(fact_final)} registros de hechos")
    print(f"\nPipeline completado exitosamente!")
