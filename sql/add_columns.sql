ALTER TABLE dim_city 
ADD COLUMN IF NOT EXISTS latitude DECIMAL(9,6),
ADD COLUMN IF NOT EXISTS longitude DECIMAL(9,6);

ALTER TABLE fact_weather
ADD COLUMN IF NOT EXISTS wind_deg INTEGER,
ADD COLUMN IF NOT EXISTS pressure INTEGER,
ADD COLUMN IF NOT EXISTS visibility INTEGER;

ALTER TABLE dim_conditions
ADD COLUMN IF NOT EXISTS icon_url_d VARCHAR(255),
ADD COLUMN IF NOT EXISTS icon_url_n VARCHAR(255);

UPDATE dim_conditions
SET icon_url_d = CASE condition_id
    WHEN 211 THEN 'https://cdn.weatherapi.com/weather/128x128/day/389.png'  
    WHEN 300 THEN 'https://cdn.weatherapi.com/weather/128x128/day/263.png'  
    WHEN 500 THEN 'https://cdn.weatherapi.com/weather/128x128/day/296.png'  
    WHEN 501 THEN 'https://cdn.weatherapi.com/weather/128x128/day/302.png' 
    WHEN 701 THEN 'https://cdn.weatherapi.com/weather/128x128/day/143.png' 
    WHEN 800 THEN 'https://cdn.weatherapi.com/weather/128x128/day/113.png'  
    WHEN 801 THEN 'https://cdn.weatherapi.com/weather/128x128/day/116.png'  
    WHEN 802 THEN 'https://cdn.weatherapi.com/weather/128x128/day/119.png'  
    WHEN 803 THEN 'https://cdn.weatherapi.com/weather/128x128/day/122.png'  
    WHEN 804 THEN 'https://cdn.weatherapi.com/weather/128x128/day/122.png'  
    ELSE NULL
END;

UPDATE dim_conditions
SET icon_url_n = CASE condition_id
    WHEN 211 THEN 'https://cdn.weatherapi.com/weather/128x128/night/389.png'
    WHEN 300 THEN 'https://cdn.weatherapi.com/weather/128x128/night/263.png'
    WHEN 500 THEN 'https://cdn.weatherapi.com/weather/128x128/night/296.png'
    WHEN 501 THEN 'https://cdn.weatherapi.com/weather/128x128/night/302.png'
    WHEN 701 THEN 'https://cdn.weatherapi.com/weather/128x128/night/143.png'
    WHEN 800 THEN 'https://cdn.weatherapi.com/weather/128x128/night/113.png'
    WHEN 801 THEN 'https://cdn.weatherapi.com/weather/128x128/night/116.png'
    WHEN 802 THEN 'https://cdn.weatherapi.com/weather/128x128/night/119.png'
    WHEN 803 THEN 'https://cdn.weatherapi.com/weather/128x128/night/122.png'
    WHEN 804 THEN 'https://cdn.weatherapi.com/weather/128x128/night/122.png'
    ELSE NULL
END;