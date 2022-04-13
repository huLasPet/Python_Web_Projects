from django import forms


class CafeForm(forms.Form):
    """The form to use when adding or editing Cafes."""
    name = forms.CharField(label="Name", max_length=250)
    map_url = forms.CharField(max_length=250)
    location = forms.CharField(max_length=250)
    img_url = forms.CharField(max_length=250)
    seats = forms.CharField(max_length=250)
    has_toilet = forms.BooleanField()
    has_wifi = forms.BooleanField()
    has_sockets = forms.BooleanField()
    coffee_price = forms.CharField(max_length=250)
    can_take_calls = forms.BooleanField()
    