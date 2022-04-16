from django import forms
from .models import Cafe


class CafeForm(forms.Form):
    """The form to use when adding or editing Cafes."""
    name = forms.CharField(label="Name", max_length=250)
    map_url = forms.URLField(label="Map link")
    location = forms.CharField(label="Location", max_length=250)
    img_url = forms.URLField(label="Picture", max_length=250)
    seats = forms.CharField(label="Seats", max_length=250)
    coffee_price = forms.CharField(label="Coffee price", max_length=250)
    has_toilet = forms.ChoiceField(label="Toilet", choices=[(False, "False"), (True, "True")])
    has_wifi = forms.ChoiceField(label="WiFi", choices=[(False, "False"), (True, "True")])
    has_sockets = forms.ChoiceField(label="Charging", choices=[(False, "False"), (True, "True")])
    can_take_calls = forms.ChoiceField(label="Can take calls", choices=[(False, "False"), (True, "True")])


class EditCafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ("name", "map_url", "location", "img_url", "seats", "coffee_price", "has_toilet", "has_wifi",
                  "has_sockets", "can_take_calls")
