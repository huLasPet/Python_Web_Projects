from django.urls import path, include

from . import views

app_name = "cafeapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('cafes/add', views.add, name='add'),
    path('cafes/edit<int:id>', views.edit, name='edit'),
    path('cafes/delete<int:id>', views.delete, name='delete'),
    path('cafes/all_cafes', views.all_cafes, name='all'),
    path('cafes/api-all', views.api_get_all, name='api-all'),
    path('cafes/api-one/<int:id>', views.api_get_one, name='api-one'),
]
