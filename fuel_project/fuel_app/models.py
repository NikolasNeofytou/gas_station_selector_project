from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} in {self.city} - {self.fuel_type}"
