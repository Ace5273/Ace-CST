
from help_classes.base_game import BaseGame
from environment import Enviroment
from arcade.color import WHITE
import os
 
class BotGame(BaseGame):
    def __init__(self):
        super().__init__(1280,800,background_color = WHITE, update_rate = 1)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        Enviroment(self.get_size()[0],self.get_size()[1])
        self.set_update_rate(1/30)


if __name__ == "__main__":
    BotGame().run()