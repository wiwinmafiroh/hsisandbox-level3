from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('diary_app.urls')),
    path('', include('weather_app.urls')),
    path('', include('poll_app.urls')),
]
