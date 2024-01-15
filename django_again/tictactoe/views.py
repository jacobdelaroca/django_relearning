from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from . import models
# Create your views here.

class JoinGame(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tictactoe/join_game.html')
    
    def post(self, request):
        game_name = self.request.POST['game_name']
        succesfully_joined = models.Game.objects.join_game(self.request.user, game_name)
        if succesfully_joined:
            return redirect('tictactoe:game', game_name=self.request.POST['game_name'])
        else:
            return redirect('tictactoe:home')

    
class CreateGame(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        game = models.Game.objects.create_game(user)
        print(game.game_name)
        return redirect('tictactoe:game', game_name=game.game_name)
    
class Game(View):
    def get(self, request, game_name):
        return render(request, 'tictactoe/game.html', {'game_name':game_name})
