from django.urls import path
from .views import WeatherForecastView, WeatherSearchForecastView

urlpatterns = [
    path("forecast/", WeatherForecastView.as_view(), name="weather-forecast"),
    path("forecast/search/", WeatherSearchForecastView.as_view(), name="weather-search-forecast"),
]