# WeatherMap-App

Setup and Run the Application
Clone the Repository

git clone https://github.com/rswarn01/WeatherMap-App.git
cd weather_app

Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install Dependencies
pip install -r requirements.txt


Configure Django Settings
Update the DATABASES configuration in weather_app/settings.py to match your PostgreSQL database settings.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
    }
}

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

Run Database Migrations
python manage.py migrate

Run the Application
python manage.py runserver


Start Celery Worker
celery -A weather_app worker --loglevel=info

Start Celery Beat (for periodic tasks) (running every 30 minutes)
celery -A weather_app beat --loglevel=info

Example Requests and Responses
Fetch Weather Data for a City
Endpoint: GET /api/weather/{city}/

Response:
{
  "city": "London",
  "temperature": 15.5,
  "description": "Clear sky",
  "timestamp": "2024-07-09T12:00:00Z"
}

Store Weather Data for a City
Endpoint: POST /api/weather/fetch/{city}/
Response:
{
  "message": "Weather data for London has been updated."
}

Fetch All Stored Weather Data
Endpoint: GET /api/weather/
Response:
[
  {
    "city": "London",
    "temperature": 15.5,
    "description": "Clear sky",
    "timestamp": "2024-07-09T12:00:00Z"
  },
  {
    "city": "New York",
    "temperature": 25.0,
    "description": "Sunny",
    "timestamp": "2024-07-09T12:00:00Z"
  }
]

Update Weather Data
Endpoint: PUT /api/weather/{id}/
{
  "temperature": 16.0,
  "description": "Partly cloudy"
}
Response:
{
  "temperature": 16.0,
  "description": "Partly cloudy"
}

Delete Weather Data
Endpoint: DELETE /api/weather/{id}/
Response:
{
  "message": "Weather data with ID 1 has been deleted."
}


Running the Application with Docker
Build and Start the Docker Containers
docker-compose up --build

Access the Application
Open your web browser and navigate to http://127.0.0.1:8000.
