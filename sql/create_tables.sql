-- -- Dimensión de condiciones climáticas
-- CREATE TABLE IF NOT EXISTS dim_conditions (
--     condition_id INTEGER PRIMARY KEY,
--     main VARCHAR(50),
--     description VARCHAR(100)
-- );

-- -- Dimensión de ciudades
-- CREATE TABLE IF NOT EXISTS dim_city (
--     city_id SERIAL PRIMARY KEY,
--     city_name VARCHAR(100) UNIQUE NOT NULL,
--     country VARCHAR(10)
-- );

-- -- Tabla de hechos del clima
-- CREATE TABLE IF NOT EXISTS fact_weather (
--     id SERIAL PRIMARY KEY,
--     city_id INTEGER REFERENCES dim_city(city_id),
--     condition_id INTEGER REFERENCES dim_conditions(condition_id),
--     date TIMESTAMP NOT NULL,
--     temp DECIMAL(5,2),
--     feels_like DECIMAL(5,2),
--     humidity INTEGER,
--     wind_speed DECIMAL(5,2),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

CREATE TABLE IF NOT EXISTS fact_forecast (
    forecast_id SERIAL PRIMARY KEY,
    city_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temp FLOAT,
    feels_like FLOAT,
    humidity INT,
    wind_speed FLOAT,
    wind_deg FLOAT,
    pressure FLOAT,
    visibility INT,
    condition_id INT NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (city_id) REFERENCES dim_city(city_id),
    FOREIGN KEY (condition_id) REFERENCES dim_conditions(condition_id)
);

CREATE INDEX IF NOT EXISTS idx_dim_city_forecast ON fact_forecast(city_id);
-- CREATE INDEX IF NOT EXISTS idx_fact_weather_date ON fact_weather(date);
-- CREATE INDEX IF NOT EXISTS idx_fact_weather_city ON fact_weather(city_id);