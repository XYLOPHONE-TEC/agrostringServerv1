from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_weather_forecast
import requests
from django.conf import settings

class WeatherForecastView(APIView):
    """
    API view to get the weather forecast for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.latitude or not user.longitude:
            return Response(
                {"error": "User location not set."},
                status=400,
            )

        forecast_data = get_weather_forecast(user.latitude, user.longitude)
        return Response(forecast_data)


class WeatherSearchForecastView(APIView):
    """
    API view to get the weather forecast for a given location.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        location_query = request.query_params.get('location')
        if not location_query:
            return Response(
                {"error": "Location parameter is required."},
                status=400,
            )

        if not settings.OPENWEATHERMAP_API_KEY:
            return Response(
                {"error": "OpenWeatherMap API key not configured."},
                status=500,
            )

        base_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location_query,
            "limit": 1,
            "appid": settings.OPENWEATHERMAP_API_KEY,
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data:
                location = data[0]
                latitude = location.get('lat')
                longitude = location.get('lon')
                forecast_data = get_weather_forecast(latitude, longitude)
                return Response(forecast_data)
            else:
                return Response(
                    {"error": "Location not found."},
                    status=404,
                )
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
