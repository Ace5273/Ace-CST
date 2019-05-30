
from help_classes.base_game import BaseGame
from environment import Enviroment, QBot

class BotGame(BaseGame):
    def __init__(self):
        super().__init__(1200,900)


if __name__ == "__main__":
    BotGame().run()