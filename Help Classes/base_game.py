"""
Platformer Game
"""
import arcade
from pyglet.event import EventDispatcher
from arcade.keyboard import KeyHelper

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
    
    def __init__(self, window: arcade.Window):
        self.window = window
        self.window.set_handlers(self)
        pass

class BaseGame(arcade.Window):

    def __init__(self, width: float = SCREEN_WIDTH, height: float = SCREEN_HEIGHT,
                 title: str = SCREEN_TITLE, fullscreen: bool = FULL_SCREEN,
                 resizable: bool = RESIZEABLE, update_rate: float = UPDATE_RATE,
                 antialiasing: bool =ANTIALIASING, background_color: tuple = BACKGROUND_COLOR):

        # Call the parent class and set up the window
        super().__init__(width, height, title, fullscreen, resizable, update_rate, antialiasing)
        arcade.set_background_color(background_color)
        self.register_event_type('on_update')
        self.is_first_time_update = True
    
    def run(self):
        arcade.run()
    
    def on_key_press(self, key, modifier):
        """
        When a key is pressed.

        Return:
            None
        """

        KeyHelper.press_key(key)
    
    def on_key_release(self, key, modifier):
        """
        When a key is released.

        Return:
            None
        """
        KeyHelper.press_key(key)

    def update(self, delta_time: float):
        """
        Move everything. Perform collision checks. Do all the game logic here.

        Args:
            :dt (float): Time interval since the last time the function was called.

        """
        # For the first time set the handlers of the window
        # to be first
        if(self.is_first_time_update):
            self.push_handlers(self)
            self.is_first_time_update = False
        
        # Dispatch an upadte to all
        self.dispatch_event('on_update', delta_time)

    def on_draw(self):
        """
        Draw everything on the screen
        """
        arcade.start_render()


BaseGame().run()