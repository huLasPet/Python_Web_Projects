from django.db import models
from django import forms
from wtforms import Form, SelectField, StringField, SubmitField
from wtforms.validators import URL, DataRequired

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

class CafeForm(Form):
    """The form to use when adding or editing Cafes."""
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Location - Google Maps link', validators=[DataRequired(), URL()])
    location = StringField('Location name', validators=[DataRequired()])
    img_url = StringField('Picture of the cafe', validators=[DataRequired(), URL()])
    seats = StringField('# of seats', validators=[DataRequired()])
    has_toilet = SelectField('Can use toilet', validators=[DataRequired()], choices=["True", "False"])
    has_wifi = SelectField('Can use Wi-Fi', validators=[DataRequired()], choices=["True", "False"])
    has_sockets = SelectField('Can charge device', validators=[DataRequired()], choices=["True", "False"])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    can_take_calls = SelectField('Can take calls', validators=[DataRequired()], choices=["True", "False"])
    submit = SubmitField('Submit')

