from help_classes.base_game import BaseGame

class CartPoleChallangeGame(BaseGame):
    def __init__(self):
        super().__init__(width= 600, height= 400)

CartPoleChallangeGame().run()