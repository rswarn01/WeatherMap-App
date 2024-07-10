import requests
from celery import shared_task
from django.utils import timezone
from .models import Weather

API_KEY = "83a09e06c654652a9578d3e816a58ecd"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@shared_task
def fetch_weather_data(city):
    try:
        response = requests.get(
            BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"}
        )
        response.raise_for_status()
        data = response.json()

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "timestamp": timezone.now(),
        }

        Weather.objects.create(**weather_data)
        print(f"Weather data for {city} saved successfully.")

    except requests.RequestException as e:
        print(f"Error fetching data for {city}: {e}")


@shared_task
def fetch_weather_data_for_cities():
    cities = ["London", "New York"]
    print(cities)
    for city in cities:
        fetch_weather_data.delay(city)
