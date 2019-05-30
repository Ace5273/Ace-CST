from help_classes.base_game import BaseGame
from arcade.draw_commands import draw_circle_filled, draw_line
from arcade.color import BLACK
import numpy

def f(x):
    return (x-1)*(x+5)


class LiamStudy(BaseGame):

    def __init__(self):
        super().__init__()
        self.set_viewport(-20,5,-20,5)
    
    def on_draw(self):

        draw_line(-2000,0,2000,0,BLACK)
        draw_line(0,-2000,0,2000,BLACK)
        for i in numpy.arange(-20, 20, 0.5):
            draw_circle_filled(i, f(i), 4, BLACK)
        # draw_circle_filled(100, f(100), 20, BLACK)
        # draw_circle_filled(200,200, 20, BLACK)

LiamStudy().run()