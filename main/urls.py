from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "main-home"),
    path('search/', views.search, name = "main-search"),
    path('settings/', views.settings, name = "main-settings"),

    path('map/', views.map, name = "main-map"),
]
