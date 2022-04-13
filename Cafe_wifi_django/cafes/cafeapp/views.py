from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Cafe, CafeForm

from django.http import HttpResponse


# Create your views here.


def index(request):
    return render(request, 'cafeapp/index.html')


def add(request):
    form = CafeForm(request.POST)
    if request.POST:
        cafe_to_add = Cafe(can_take_calls=bool(form.can_take_calls.data),
                           coffee_price=form.coffee_price.data,
                           has_sockets=bool(form.has_sockets.data),
                           has_toilet=bool(form.has_toilet.data),
                           has_wifi=bool(form.has_wifi.data),
                           img_url=form.img_url.data,
                           location=form.location.data,
                           map_url=form.map_url.data,
                           name=form.name.data,
                           seats=form.seats.data)
        print(cafe_to_add)
        return render(request, 'cafeapp/all.html')
        # try:
        #     db_sqlalchemy.session.add(cafe_to_add)
        #     db_sqlalchemy.session.commit()
        #     return redirect(url_for('cafes'))
        # except sqlalchemy.exc.IntegrityError:
        #     return jsonify(respnse={"error": "Record already exists"})
    return render(request, 'cafeapp/add.html', {'form': form})


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
