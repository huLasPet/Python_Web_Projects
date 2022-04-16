from django.urls import path

from . import views

app_name = "cafeapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('cafes/add', views.add, name='add'),
    path('cafes/edit<int:id>', views.edit, name='edit'),
    path('cafes/delete<int:id>', views.delete, name='delete'),
    path('cafes/all_cafes', views.all_cafes, name='all'),
]