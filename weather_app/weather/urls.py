from django.urls import path
from .views import (
    WeatherListView,
    WeatherDetailView,
    FetchWeatherView,
    FetchAndStoreWeatherView,
)

urlpatterns = [
    path("weather/", WeatherListView.as_view(), name="weather-list"),
    path("weather/<int:pk>/", WeatherDetailView.as_view(), name="weather-detail"),
    path("weather/<str:city>/", FetchWeatherView.as_view(), name="fetch-weather"),
    path(
        "weather/fetch/<str:city>/",
        FetchAndStoreWeatherView.as_view(),
        name="fetch-and-store-weather",
    ),
]
