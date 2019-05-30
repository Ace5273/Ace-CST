from help_classes.base_game import GameObject
from help_classes.vector import Point 
from help_classes.keyboard import ArrowKeyboard, WASDKeyboard
from arcade.draw_commands import draw_rectangle_filled
from arcade.color import ARYLIDE_YELLOW
from ball import Ball



class Tile(GameObject):

    def __init__(self, ball : Ball):
        super().__init__()

        self.ball = ball
        self.width = 100
        self.height = 35
        self.position = Point(1000, 700)
        self.color = ARYLIDE_YELLOW
        self.destroyed = False
    
    def on_draw(self):
        if self.destroyed:
            return
        draw_rectangle_filled(self.position.x, self.position.y, self.width, self.height, self.color)
    
    def on_update(self, delta_time):
        
        if self.destroyed:
            return

        

        # if self.ball.position.x + self.ball.radius >= self.position.x - self.width / 2 and \
        #     self.ball.position.y + self.ball.radius >= self.position.y -self.height / 2:
        #     self.ball.flip_y()
        #     self.destroyed = True
