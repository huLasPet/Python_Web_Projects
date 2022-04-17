from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view
from .models import Cafe
from .forms import CafeForm, EditCafeForm
from rest_framework.response import Response
from rest_framework import status
from .serializers import CafeSerializer
from rest_framework.views import APIView


def index(request):
    return render(request, 'cafeapp/index.html')


def add(request):
    form = CafeForm()
    if request.method == 'POST':
        cafe_to_add = Cafe(can_take_calls=request.POST["can_take_calls"],
                           coffee_price=request.POST["coffee_price"],
                           has_sockets=request.POST["has_sockets"],
                           has_toilet=request.POST["has_toilet"],
                           has_wifi=request.POST["has_wifi"],
                           img_url=request.POST["img_url"],
                           location=request.POST["location"],
                           map_url=request.POST["map_url"],
                           name=request.POST["name"],
                           seats=request.POST["seats"])
        cafe_to_add.save()
        return render(request, 'cafeapp/index.html')
    return render(request, 'cafeapp/add.html', {'form': form})


def all_cafes(request):
    cafes = Cafe.objects.all()
    context = {'cafes': cafes}
    return render(request, 'cafeapp/all.html', context)


def edit(request, id):
    cafe_to_edit = get_object_or_404(Cafe, id=id)
    if request.method == 'POST':
        cafe_to_edit.can_take_calls = request.POST["can_take_calls"]
        cafe_to_edit.coffee_price = request.POST["coffee_price"]
        cafe_to_edit.has_sockets = request.POST["has_sockets"]
        cafe_to_edit.has_toilet = request.POST["has_toilet"]
        cafe_to_edit.has_wifi = request.POST["has_wifi"]
        cafe_to_edit.img_url = request.POST["img_url"]
        cafe_to_edit.location = request.POST["location"]
        cafe_to_edit.map_url = request.POST["map_url"]
        cafe_to_edit.name = request.POST["name"]
        cafe_to_edit.seats = request.POST["seats"]
        cafe_to_edit.save()
        return HttpResponseRedirect(reverse('cafeapp:all'))
    form = EditCafeForm(instance=cafe_to_edit)
    return render(request, 'cafeapp/edit.html', {'form': form, 'id': id})


def delete(request, id):
    cafe_id = Cafe.objects.get(pk=id)
    cafe_id.delete()
    return HttpResponseRedirect(reverse('cafeapp:all'))


@api_view(('GET',))
def api_get_all(*args):
    cafes = Cafe.objects.all()
    serializer = CafeSerializer(cafes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(('GET',))
def api_get_one(request, id):
    cafes = Cafe.objects.get(pk=id)
    serializer = CafeSerializer(cafes)
    return Response(serializer.data, status=status.HTTP_200_OK)
