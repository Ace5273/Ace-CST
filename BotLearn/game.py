
from help_classes.base_game import BaseGame
from environment import Enviroment
from arcade.color import WHITE

class BotGame(BaseGame):
    def __init__(self):
        super().__init__(800,600,background_color = WHITE, update_rate = 1/2)
        Enviroment(self.get_size()[0],self.get_size()[1])


if __name__ == "__main__":
    BotGame().run()