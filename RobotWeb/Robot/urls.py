from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Adaugă alte rute aici
]