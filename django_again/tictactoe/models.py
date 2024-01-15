from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# Create your models here.

class GameManager(models.Manager):
    def create_game(self, user):
        game = None
        while True:
            game_name = get_random_string(length=10, allowed_chars='qwertyuiopasdfghjklzxcvbnm')
            game, c = self.model.objects.get_or_create(game_name=game_name)
            if not c:
                continue
            else:
                game.board = {
                    'game_name': game_name,
                    'board': [
                        [' ', ' ', ' '],
                        [' ', ' ', ' '],
                        [' ', ' ', ' '],
                    ],
                    'turn': 'x'
                    }
                game.player1 = user
                game.player2 = user
                game.save()
            
            return game
    
    def join_game(self, user, game_name):
        game = self.model.objects.get(game_name=game_name)
        board = game.board
        if game.player1 == user:
            return True, 'x', board
        elif game.player2 == user:
            return True, 'o', board
        # if player 1 and 2 are the same, that means there are no player 2 yet, so set player to to user
        elif game.player1 == game.player2:
            game.player2 = user
            game.save()
            return True, 'o', board
        # if use is neither player 1 or 2, reject
        else:
            return False, ' ', board


        

class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1', null=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2', null=True)
    board = models.JSONField(null=True)
    #true for player one false for player 2
    winner = models.BooleanField(null=True)
    game_name = models.CharField(max_length=20, null=True)

    objects = GameManager()
