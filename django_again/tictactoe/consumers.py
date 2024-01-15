from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game
import json

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = f'game_{self.game_name}'
        succesfully_joined, self.player_symbol, board = await self.join_game(user, self.game_name)
        if succesfully_joined:
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'initialize',
                'player_symbol': self.player_symbol,
                'board': board['board'],
                'turn': board['turn']
            }))
            win = self.check_win(board['board'])
            turn = board['turn']
            await self.channel_layer.group_send(
            self.game_group_name, {
                'type': 'board_update',
                'board': board['board'],
                'winner': win,
                'turn': turn,
            }
        )
            await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        else:
            await self.close()
        # clears board when reconnect or connect
        # remove later testing only
        # game = await self.get_game(self.game_name)
        # game.board['board'] = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
        # await self.save_game(game)
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        move = data['move']
        game = await self.get_game(self.game_name)
        board = game.board['board']
        turn = game.board['turn']
        valid = self.validate_move(move, board, turn)
        win = None
        if valid:
            x, y = move
            board[x][y] = self.player_symbol
            game.board['board'] = board
            game = await self.save_game(game)
            print(game.board)
            win = self.check_win(board)
            turn = game.board['turn']
                
        else:
            print('move not valid, handle later')
        print(win)

        await self.channel_layer.group_send(
            self.game_group_name, {
                'type': 'board_update',
                'board': board,
                'winner': win,
                'turn': turn,
            }
        )

    async def board_update(self, event):
        board_update = {
            'type': 'update',
            'board': event['board'],
            'winner': event['winner'],
            'turn': event['turn'],
        }

        await self.send(text_data=json.dumps(board_update))
        

    async def disconnect(self, code):
        pass

    def validate_move(self, move, board, turn):
        x,y = move
        if not self.player_symbol == turn: return False
        if not 0 <= x <= 3: return False
        if not 0 <= y <= 3: return False
        if not board[x][y] == ' ': return False
        return True

    def check_win(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return board[i][0]  # Row win
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return board[0][i]  # Column win

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]  # Diagonal win
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]  # Diagonal win

        return ' '  # No winner yet

    @database_sync_to_async
    def save_game(self, game):
        turn = 'x' if game.board['turn'] == 'o' else 'o'
        game.board['turn'] = turn
        game.save()
        return game

    @database_sync_to_async
    def join_game(self, user=None, game_name=None):
        return  Game.objects.join_game(user, game_name)
    
    @database_sync_to_async
    def get_game(self, game_name):
        return Game.objects.get(game_name=game_name)