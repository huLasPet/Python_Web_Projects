from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Cafe
from .forms import CafeForm

from django.http import HttpResponse


# Create your views here.


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
        print(cafe_to_add)
        cafe_to_add.save()
        return render(request, 'cafeapp/index.html')
        # try:
        #     db_sqlalchemy.session.add(cafe_to_add)
        #     db_sqlalchemy.session.commit()
        #     return redirect(url_for('cafes'))
        # except sqlalchemy.exc.IntegrityError:
        #     return jsonify(respnse={"error": "Record already exists"})
    return render(request, 'cafeapp/add.html', {'form': form.fields})


def all(request):
    cafes = Cafe.objects.all()
    context = {'cafes': cafes}
    return render(request, 'cafeapp/all.html', context)


def edit(request, id):
    cafe_id = Cafe.objects.get(pk=id)
    return render(request, 'cafeapp/edit.html')


def delete(request, id):
    cafe_id = Cafe.objects.get(pk=id)
    cafe_id.delete()
    return HttpResponseRedirect(reverse('cafeapp:all'))
