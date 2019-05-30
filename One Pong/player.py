from help_classes.base_game import GameObject
from help_classes.vector import Point 
from help_classes.keyboard import ArrowKeyboard, WASDKeyboard
from arcade.draw_commands import draw_rectangle_filled
from arcade.color import WHITE

class Player(GameObject):

    def __init__(self, screen_width):
        super().__init__()
        self.keyboard = ArrowKeyboard
        self.color = WHITE
        self.width = 125
        self.height = 25
        self.position = Point(200, 200)
        self.velocity = 0
        self.force = 10
        self.screen_width = screen_width

    def on_draw(self):

        draw_rectangle_filled(self.position.x, self.position.y, 
                                self.width, self.height, self.color)
    
    def on_update(self, delta_time):
        
        if self.keyboard.is_key_pressed_down('right') ^ self.keyboard.is_key_pressed_down('left'):
            
            if self.keyboard.is_key_pressed_down('right') and self.position.x + self.width / 2 < self.screen_width:

                self.velocity = self.force
                
            elif self.keyboard.is_key_pressed_down('left') and self.position.x - self.width / 2 > 0:

                self.velocity = -self.force
            
            else: 
                self.velocity = 0
        
        else:
            self.velocity = 0


        self.position.x += self.velocity
