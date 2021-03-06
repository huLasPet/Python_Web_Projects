# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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

