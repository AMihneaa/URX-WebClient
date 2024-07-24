from django.urls import path
from . import views

urlpatterns = [

    path('configure/', views.Configure, name='Test'),
    path('capture/', views.Capture, name='Test2')
]