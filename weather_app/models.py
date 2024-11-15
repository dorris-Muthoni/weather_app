from django.db import models

# Create your models here.
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)  # Optional field for country
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50)  # Stores icon code from the weather API
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather in {self.city.name} on {self.date_recorded}"

class UserQuery(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    query_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query for {self.city.name} on {self.query_date}"

