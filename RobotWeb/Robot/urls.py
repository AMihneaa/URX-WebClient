from django.urls import path
from . import views

urlpatterns = [
    path('initRobot/<str:ip>/', views.initRobot, name='initRobot'),
    path('getPosition/', views.getPosition, name='getPosition'),
    path('moveInit/', views.moveInitialPosition, name='moveInit'),
    path('movePosition/', views.movePosition, name='movePosition'),
]