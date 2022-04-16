from django.db import models

# Create your models here.


class Cafe(models.Model):
    name = models.CharField(max_length=250)
    map_url = models.CharField(max_length=250)
    img_url = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    seats = models.CharField(max_length=250)
    coffee_price = models.CharField(max_length=250)
    has_sockets = models.BooleanField(default=False, choices=[(False, "False"), (True, "True")])
    has_toilet = models.BooleanField(default=False, choices=[(False, "False"), (True, "True")])
    has_wifi = models.BooleanField(default=False, choices=[(False, "False"), (True, "True")])
    can_take_calls = models.BooleanField(default=False, choices=[(False, "False"), (True, "True")])


    def __str__(self):
        return self.name


