from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "main-home"),
    path('search/', views.search, name = "main-search"),
    path('settings/', views.settings, name = "main-settings"),

    #path to view map
    path('maps/<str:username>/<str:map_name>/', views.map, name='main-map'),

    #path to view pin
    path('maps/<str:username>/<str:map_name>/<str:pin_name>', views.pin, name='main-pin'),

    #path to edit pin
    path('maps/<str:username>/<str:map_name>/<str:pin_name>/edit', views.edit_pin, name='edit-pin'),

    #path to edit pin
    path('user/<str:username>/', views.user_profile, name='user-profile'),

]
