import arcade
import math

from help_classes.base_game import GameObject
from help_classes.vector import Point
from help_classes.keyboard import BaseKeyboard

GRAVITY = 2

class Pole(GameObject):

    def __init__(self, x, y):
        super().__init__(Point(x,y))
        self.length = 500
        self.size = 10
        self._angle = 270
        self._ang_velocity  = 0
        self.mass = 0
    
    @property
    def angle(self):
        return math.radians(self._angle)
    
    @angle.setter
    def angle(self, value):
        self._angle = math.degrees(value)
    
    @property
    def ang_velocity(self):
        return math.radians(self._ang_velocity)
    
    @ang_velocity.setter
    def ang_velocity(self, value):
        self._ang_velocity = math.degrees(value)

    def on_draw(self):
        # arcade.draw_rectangle_filled(self.position.x, self.position.y + self.width /2, \
        # self.width, self.height, arcade.color.BROWN_NOSE, tilt_angle= self.pole_angle)
        self.position.draw_line(self.end_of_pole, arcade.color.BROWN_NOSE, self.size)
        self.draw_position_point(color= arcade.color.RED,size=10)
        self.end_of_pole.draw(color= arcade.color.RED,size=10)
    
    def on_update(self, delta_time):
        self.ang_velocity += (GRAVITY / self.length) * math.sin(self.angle - math.radians(90))
        self.angle += self.ang_velocity
        self.end_of_pole = self.position + \
             Point(math.cos(self.angle) * self.length, math.sin(self.angle) * self.length)
            
        # super().on_update(delta_time)

class Cart(GameObject):

    def __init__(self, keyboard : BaseKeyboard, x, y):
        self.keyboard = keyboard
        self.pole = Pole(x, y)
        self.Mass = 1
        self.accelartion = 0
        self.velocity = 0
        # self.force = self.Mass * self.accelartion

        self.width = 70
        self.height = 50
        super().__init__(Point(x,y))
    
    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height, arcade.color.SILVER)
    
    def on_update(self, delta_time):
        self.force = self.Mass * self.accelartion
        self.accelartion = -self.pole.mass * GRAVITY * math.sin(self.pole.angle) * math.cos(self.pole.angle)
        self.accelartion += self.pole.mass * self.pole.length * self.pole.ang_velocity ** 2 * math.sin(self.pole.angle) + self.force
        self.accelartion /= self.Mass + (1 - math.cos(self.pole.angle)**2)

        self.velocity += self.accelartion
        self.position.x += self.velocity
        self.pole.position.x = self.position.x
        pass
        # self.pole_ang_velocity += (GRAVITY / self.pole_length) * math.sin(math.radians(self.pole_angle - 90))
        # self.pole_angle += self.pole_ang_velocity
        # self.end_of_pole = self.position + \
        #      Point(math.cos(math.radians(self.pole_angle)) * self.pole_length, math.sin(math.radians(self.pole_angle)) * self.pole_length)

        # if (self.keyboard.is_key_pressed_down('left') ^ self.keyboard.is_key_pressed_down('right')):

        #     if self.keyboard.is_key_pressed_down('left') and (self.position.x - self.width/2) > 0:
        #         self.velocity.x = -3
            
        #     elif self.keyboard.is_key_pressed_down('right') and (self.position.x + self.width/2) < 600:
        #         self.velocity.x = 3

        #     else:
        #         self.velocity.x = 0
        
        # else:
        #     self.velocity.x = 0
            
        # super().on_update(delta_time)

        # self.pole.position = self.position
