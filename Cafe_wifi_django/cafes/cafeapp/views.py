from django.shortcuts import render
from .models import Cafe
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'cafeapp/index.html')

def add(request):
    return render(request, 'cafeapp/add.html')

def all(request):
    cafes = Cafe.objects.all()
    context = {'cafes': cafes}
    return render(request, 'cafeapp/all.html', context)

def edit(request, id):
    cafe_id = Cafe.objects.get(pk=id)
    return render(request, 'cafeapp/edit.html')
