from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='diary'),
    path('add/', views.add, name='add'),
]