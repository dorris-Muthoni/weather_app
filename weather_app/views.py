from django.shortcuts import render, HttpResponse
from .models import City, WeatherData, UserQuery

# Helper function to get or create a City instance
def get_or_create_city(city_name):
    city, created = City.objects.get_or_create(name=city_name)
    return city

# Helper function to save weather data
def save_weather_data(city, temperature, description, icon):
    WeatherData.objects.create(
        city=city,
        temperature=temperature,
        description=description,
        icon=icon
    )

# Helper function to save a user query
def save_user_query(city):
    UserQuery.objects.create(city=city)

# Helper function to get recent weather data for a city
def get_recent_weather(city, limit=5):
    return WeatherData.objects.filter(city=city).order_by('-date_recorded')[:limit]

# Helper function to get recent user queries
def get_recent_queries(limit=5):
    return UserQuery.objects.order_by('-query_date')[:limit]

# Main weather view
def weather_view(request):
    api_key = 'YOUR_API_KEY'
    city_name = request.GET.get('city', 'Nairobi')

    # Use helper function to get or create city
    city = get_or_create_city(city_name)

    # Save user query
    save_user_query(city)

    # Fetch weather data from API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': city_name,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        # Save the weather data using helper function
        save_weather_data(
            city=city,
            temperature=weather['temperature'],
            description=weather['description'],
            icon=weather['icon']
        )
    else:
        weather = {'error': 'City not found or API limit reached.'}

    # Retrieve recent weather records and recent queries using helper functions
    recent_weather = get_recent_weather(city)
    recent_queries = get_recent_queries()

    context = {
        'weather': weather,
        'recent_weather': recent_weather,
        'recent_queries': recent_queries
    }
    return render(request, 'weather/weather.html', context)



