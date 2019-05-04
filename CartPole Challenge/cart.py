import arcade

from help_classes.base_game import GameObject
from help_classes.vector import Point
from help_classes.keyboard import BaseKeyboard

GRAVITY = 9.8

class Pole(GameObject):

    def __init__(self, x, y):
        super().__init__(Point(x,y))
        self.width = 10
        self.height = 60

    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(self.position.x - self.width/2, self.position.y, self.width, self.height, arcade.color.BROWN_NOSE)
        self.draw_position_point(color= arcade.color.RED,size=10)
    
    def on_update(self, delta_time):

        # if self.keyboard.is_key_pressed_down('left') ^ self.keyboard.is_key_pressed_down('right'):

        #     if self.keyboard.is_key_pressed_down('left'):
        #         self.velocity.x = -3
            
        #     elif self.keyboard.is_key_pressed_down('right'):
        #         self.velocity.x = 3
        
        # else:
        #     self.velocity.x = 0
            
        super().on_update(delta_time)

class Cart(GameObject):

    def __init__(self, keyboard : BaseKeyboard, x, y):
        self.keyboard = keyboard
        self.width = 70
        self.height = 50
        # self.pole = Pole(x, y)
        super().__init__(Point(x,y))
    
    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height, arcade.color.SILVER)
        self.draw_position_point(color= arcade.color.RED,size=10)
    
    def on_update(self, delta_time):

        if (self.keyboard.is_key_pressed_down('left') ^ self.keyboard.is_key_pressed_down('right')):

            if self.keyboard.is_key_pressed_down('left') and (self.position.x - self.width/2) > 0:
                self.velocity.x = -3
            
            elif self.keyboard.is_key_pressed_down('right') and (self.position.x + self.width/2) < 600:
                self.velocity.x = 3

            else:
                self.velocity.x = 0
        
        else:
            self.velocity.x = 0
            
        super().on_update(delta_time)

        self.pole.position = self.position
