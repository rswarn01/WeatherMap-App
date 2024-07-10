from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Weather
from .serializers import WeatherSerializer
from .tasks import fetch_weather_data


class WeatherListView(generics.ListCreateAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    @swagger_auto_schema(
        operation_description="Fetch all weather data",
        responses={200: WeatherSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WeatherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    @swagger_auto_schema(
        operation_description="Get weather data by ID",
        responses={200: WeatherSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update weather data by ID",
        responses={200: WeatherSerializer()},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete weather data by ID",
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class FetchWeatherView(APIView):
    @swagger_auto_schema(
        operation_description="Fetch weather data for a city",
        manual_parameters=[
            openapi.Parameter(
                "city",
                openapi.IN_PATH,
                description="City name",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: WeatherSerializer()},
    )
    def get(self, request, city, *args, **kwargs):
        weather = (
            Weather.objects.filter(city__iexact=city).order_by("-timestamp").first()
        )
        if weather:
            serializer = WeatherSerializer(weather)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Weather data not found for the specified city."},
            status=status.HTTP_404_NOT_FOUND,
        )


class FetchAndStoreWeatherView(APIView):
    @swagger_auto_schema(
        operation_description="Fetch and store weather data for a city",
        manual_parameters=[
            openapi.Parameter(
                "city",
                openapi.IN_PATH,
                description="City name",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={201: openapi.Response("Weather data updated")},
    )
    def post(self, request, city, *args, **kwargs):
        fetch_weather_data.delay(city)
        return Response(
            {"message": f"Weather data for {city} has been requested."},
            status=status.HTTP_202_ACCEPTED,
        )
