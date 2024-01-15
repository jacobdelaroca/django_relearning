from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name='tictactoe'

urlpatterns = [
    path('', TemplateView.as_view(template_name='tictactoe/home.html'),name='home'),
    path('join', JoinGame.as_view(),name='join_game'),
    path('create-game', CreateGame.as_view(),name='create_game'),
    path('game/<str:game_name>/', Game.as_view(),name='game'),
]