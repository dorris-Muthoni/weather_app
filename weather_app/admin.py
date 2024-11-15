from django.contrib import admin

# Register your models here.

from .models import City, WeatherData, UserQuery

admin.site.register(City)
admin.site.register(WeatherData)
admin.site.register(UserQuery)
