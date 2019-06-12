from help_classes.base_game import BaseGame
from help_classes.keyboard import ArrowKeyboard
from cart import BotCart, Cart, Pole, Enviroment

class CartPoleChallangeGame(BaseGame):
    def __init__(self):
        super().__init__(width= 1200, height= 400)
        Enviroment()
        # Pole(300,200)
        Cart(ArrowKeyboard)
        # AICart()
        # BotCart()

CartPoleChallangeGame().run()