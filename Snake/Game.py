from help_classes.base_game import BaseGame
from environment import Environment
from arcade.color import BLACK

class Snake(BaseGame):
    def __init__(self, width, height):
        super().__init__(width, height, background_color=BLACK)
        self.set_update_rate(1/6)
        Environment(width, height, 10, 10)

Snake(600, 600).run()