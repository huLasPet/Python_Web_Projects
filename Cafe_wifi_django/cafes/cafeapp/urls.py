from django.urls import path

from . import views

app_name = "cafeapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('cafes/add', views.add, name='add'),
    path('cafes/edit<int:id>', views.edit, name='edit'),
    path('cafes/all', views.all, name='all'),
]