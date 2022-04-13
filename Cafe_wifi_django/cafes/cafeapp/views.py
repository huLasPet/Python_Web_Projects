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
    print(form.fields)
    if request.method == 'POST':
        # cafe_to_add = Cafe(can_take_calls=form.fields.can_take_calls,
        #                    coffee_price=form.fields.coffee_price.data,
        #                    has_sockets=form.fields.has_sockets.data,
        #                    has_toilet=form.fields.has_toilet.data,
        #                    has_wifi=form.fields.has_wifi.data,
        #                    img_url=form.fields.img_url.data,
        #                    location=form.fields.location.data,
        #                    map_url=form.fields.map_url.data,
        #                    name=form.fields.name.data,
        #                    seats=form.fields.seats.data)
        print(request.POST["seats"])
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
