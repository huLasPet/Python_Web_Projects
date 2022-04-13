from django.db import models
from django import forms

# Create your models here.


class Cafe(models.Model):
    name = models.CharField(max_length=250)
    map_url = models.CharField(max_length=250)
    img_url = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    has_sockets = models.BooleanField(default=False)
    has_toilet = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    can_take_calls = models.BooleanField(default=False)
    seats = models.CharField(max_length=250)
    coffee_price = models.CharField(max_length=250)

    def __str__(self):
        return self.name


# class CafeForm(forms.Form):
#     """The form to use when adding or editing Cafes."""
#     name = forms.CharField(initial='Cafe name')
#     map_url = forms.URLField(initial='Location - Google Maps link')
#     location = forms.CharField(initial='Location name')
#     img_url = forms.CharField(initial='Picture of the cafe')
#     seats = forms.CharField(initial='# of seats')
#     has_toilet = SelectField('Can use toilet')
#     has_wifi = SelectField('Can use Wi-Fi')
#     has_sockets = SelectField('Can charge device')
#     coffee_price = forms.CharField(initial='Coffee price')
#     can_take_calls = SelectField('Can take calls')
#     submit = SubmitField()
