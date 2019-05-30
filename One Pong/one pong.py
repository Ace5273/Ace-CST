from help_classes.base_game import BaseGame
from arcade.color import BLACK
from player import Player
from ball import Ball
from tile import Tile

class OnePong(BaseGame):
    def __init__(self):
        super().__init__(background_color= BLACK )
        width, height = self.get_size()
        player = Player(width)
        ball = Ball(player, width, height)
        Tile(ball)

OnePong().run()
    
