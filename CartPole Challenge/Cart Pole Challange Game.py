from help_classes.base_game import BaseGame
from help_classes.keyboard import ArrowKeyboard
from cart import Cart

class CartPoleChallangeGame(BaseGame):
    def __init__(self):
        super().__init__(width= 600, height= 400)
        Cart(ArrowKeyboard, 300, 200)

CartPoleChallangeGame().run()