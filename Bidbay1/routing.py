from django.urls import path
from .consumers import *

wsPattern = [path("ws/messages/<str:room_name>/<str:user_name>/", Bidbay1Consumer.as_asgi())]