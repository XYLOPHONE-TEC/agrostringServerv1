import requests
from django.conf import settings

def get_weather_forecast(latitude, longitude):
    """
    Fetches the weather forecast for a given latitude and longitude.
    """
    if not settings.OPENWEATHERMAP_API_KEY:
        return {"error": "OpenWeatherMap API key not configured."}

    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Use metric units (Celsius)
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}