from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = 'chat'
urlpatterns = [
    path('', TemplateView.as_view(template_name='chat/home.html'), name='home'),
    path('room/<str:room_name>/', Room.as_view(), name='room'),
    path('create-room/', CreateRoom.as_view(), name='create_room'),
]