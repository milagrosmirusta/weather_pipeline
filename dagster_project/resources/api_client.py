import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_base = "https://api.openweathermap.org/data/2.5/forecast"
    
    def get_weather(self, city: str) -> dict:
        """Trae datos del clima para una ciudad"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Celsius
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_forecast(self, city: str) -> dict:
        """Pronóstico 5 días / 3 horas"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        r = requests.get(self.forecast_base, params=params)
        r.raise_for_status()
        return r.json()
    
    def get_multiple_cities(self, cities: list) -> list:
        """Trae datos de múltiples ciudades"""
        results = []
        for city in cities:
            try:
                data = self.get_weather(city)
                results.append(data)
            except Exception as e:
                print(f"Error obteniendo data de {city}: {e}")
        
        return results