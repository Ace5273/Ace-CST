from help_classes.base_game import GameObject
from help_classes.keyboard import BotKeyboard, BaseBotKeyboard
from arcade.draw_commands import load_texture, draw_texture_rectangle
from help_classes.content_manager import LoadSprite, Sprite
from abc import ABC, abstractmethod

class MatrixBasedGameObject(GameObject, ABC):
    
    def __init__(self, pos_x, pos_y, environment):
        super().__init__()
        self.environment = environment
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    @property
    @abstractmethod
    def pos_x(self):
        pass
    
    @pos_x.setter
    @abstractmethod
    def pos_x(self, value):
        pass

    @property
    @abstractmethod
    def pos_y(self):
        pass
    
    @pos_y.setter
    @abstractmethod
    def pos_y(self, value):
        pass
    
    @property
    def width(self):
        return self.environment.width
    
    @property
    def height(self):
        return self.environment.height
    
    @property
    def rows(self):
        return self.environment.rows
    
    @property
    def cols(self):
        return self.environment.cols


class SpriteMatrixObject(MatrixBasedGameObject):
    
    def __init__(self, pos_x, pos_y, environment, url):

        self.sprite : Sprite = LoadSprite(url)
        super().__init__(pos_x, pos_y, environment)

        # self.sprite._set_center_x((pos_x+0.5)*mat_width / mat_cols)
        # self.sprite._set_center_y((pos_y+0.5)*mat_height / mat_rows)

        self.sprite._set_width(self.width / self.cols)
        self.sprite._set_height(self.height / self.rows)

    @property
    def pos_x(self):
        return self.sprite._get_center_x() * self.cols / self.width - 0.5
    
    @pos_x.setter
    def pos_x(self, value):
        if value >= 0 and value < self.cols:
            self.sprite._set_center_x((value + 0.5)*self.width / self.cols)

    @property
    def pos_y(self):
        return self.sprite._get_center_y() * self.rows / self.height - 0.5
    
    @pos_y.setter
    def pos_y(self, value):
        if value >= 0 and value < self.rows:
            self.sprite._set_center_y((value + 0.5)*self.height / self.rows)

    def on_draw(self):
        self.sprite.draw()

class PlayerMatrixObject(SpriteMatrixObject):
    def __init__(self, pos_x, pos_y, environment, url, keyboard: BaseBotKeyboard):
        super().__init__(pos_x, pos_y, environment, url)
        self.keyboard = keyboard
    
    def on_update(self,delta_time):
        if self.keyboard.is_key_pressing('up'):
            self.pos_y += 1
        
        if self.keyboard.is_key_pressing('down'):
            self.pos_y -= 1

        if self.keyboard.is_key_pressing('right'):
            self.pos_x += 1
        
        if self.keyboard.is_key_pressing('left'):
            self.pos_x -= 1

