from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_weather_forecast

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
