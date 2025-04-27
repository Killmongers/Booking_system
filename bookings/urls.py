from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('search/', views.search_flights, name='search_flights'),
    path('hotel/', views.hotel_search, name='hotel_search'),
    path('package/', views.package_search, name='package_search'),

]
