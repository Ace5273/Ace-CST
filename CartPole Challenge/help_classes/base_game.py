"""
Platformer Game
"""
import arcade
from .vector import Vector, Point
from pyglet.event import EventDispatcher
from .keyboard import KeyHelper, WASDKeyboard, ArrowKeyboard

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "BaseGame"
FULL_SCREEN = False
RESIZEABLE  = False
UPDATE_RATE = 1/60
ANTIALIASING = True
BACKGROUND_COLOR = arcade.csscolor.CORNFLOWER_BLUE

class GameObject():
    
    def __init__(self):
        GameObject.window.push_handlers(self)
        # self._position = Point.duplicate(position)
        # self._velocity = Vector(0, 0, velocity.x, velocity.y)
    
    # @property
    # def position(self) -> Point:
    #     return self._position
    
    # @position.setter
    # def position(self, position: Point):
    #     self._position = position
    
    # @property
    # def velocity(self):
    #     return self._velocity.end_point
    
    # @velocity.setter
    # def velocity(self, velocity: Point):
    #     self._velocity.end_point = velocity
    
    # @property
    # def velocity_length(self):
    #     self._velocity.length

    # def on_update(self, delta_time):
    #     pass
    #       self.position += self.velocity
    
    # def draw_position_point(self, color: arcade.Color = arcade.color.BLACK, size: float = 10):
    #     self.position.draw(color, size)
    
    # def draw_velocity_point(self, color: arcade.Color = arcade.color.BLACK, size: float = 10):
    #     (self.position + self.velocity).draw(color, size)
    
    # def draw_direction_line(self, color: arcade.Color = arcade.color.BLACK, size: float = 5):
    #     self.position.draw_line(self.position + self.velocity, color, size)

class BaseGame(arcade.Window):

    def __init__(self, width: float = SCREEN_WIDTH, height: float = SCREEN_HEIGHT,
                 title: str = SCREEN_TITLE, fullscreen: bool = FULL_SCREEN,
                 resizable: bool = RESIZEABLE, update_rate: float = UPDATE_RATE,
                 antialiasing: bool = ANTIALIASING, background_color: tuple = BACKGROUND_COLOR):

        # Call the parent class and set up the window
        super().__init__(width, height, title, fullscreen, resizable, update_rate, antialiasing)
        arcade.set_background_color(background_color)
        self.register_event_type('on_update')
        GameObject.window = self
    
    def run(self):
        self.push_handlers(self)
        self.set_handler('on_draw', self.start_draw)
        arcade.run()
    
    def on_key_press(self, key, modifier):
        """
        When a key is pressed.

        Return:
            None
        """

        KeyHelper.press_key(key)
        return True
    
    def on_key_release(self, key, modifier):
        """
        When a key is released.

        Return:
            None
        """

        KeyHelper.release_key(key)
        return True

    def update(self, delta_time: float):
        """
        Move everything. Perform collision checks. Do all the game logic here.

        Args:
            :dt (float): Time interval since the last time the function was called.

        """
        
        # Dispatch an upadte to all
        self.dispatch_event('on_update', delta_time)

        KeyHelper.update()
    
    def start_draw(self):
        """
        Draw everything on the screen
        """
        arcade.start_render()
