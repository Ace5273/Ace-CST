from help_classes.base_game import GameObject
from help_classes.keyboard import BotKeyboard, BaseBotKeyboard
from arcade.draw_commands import load_texture, draw_texture_rectangle
from help_classes.content_manager import LoadSprite, Sprite
from abc import ABC, abstractmethod

class MatrixBasedGameObject(GameObject, ABC):
    
    def __init__(self, pos_x : int, pos_y :int, environment):
        super().__init__()
        self.environment = environment
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    @property
    @abstractmethod
    def pos_x(self) -> int:
        pass
    
    @pos_x.setter
    @abstractmethod
    def pos_x(self, value : int):
        pass

    @property
    @abstractmethod
    def pos_y(self) -> int:
        pass
    
    @pos_y.setter
    @abstractmethod
    def pos_y(self, value : int):
        pass
    
    @property
    def env_width(self):
        return self.environment.width
    
    @property
    def env_height(self):
        return self.environment.height
    
    @property
    def mat_rows(self):
        return self.environment.rows
    
    @property
    def mat_cols(self):
        return self.environment.cols


class SpriteMatrixObject(MatrixBasedGameObject, ABC):
    
    def __init__(self, pos_x, pos_y, environment, url):

        self.sprite : Sprite = LoadSprite(url)
        super().__init__(pos_x, pos_y, environment)

        self.sprite._set_width(self.env_width / self.mat_cols)
        self.sprite._set_height(self.env_height / self.mat_rows)

    @property
    def pos_x(self) -> int:
        return int(self.sprite._get_center_x() * self.mat_cols / self.env_width - 0.5)
    
    @pos_x.setter
    def pos_x(self, value:int):
        if value >= 0 and value < self.mat_cols:
            self.sprite._set_center_x((value + 0.5)*self.env_width / self.mat_cols)

    @property
    def pos_y(self) -> int:
        return int(self.sprite._get_center_y() * self.mat_rows / self.env_height - 0.5)
    
    @pos_y.setter
    def pos_y(self, value: int):
        if value >= 0 and value < self.mat_rows:
            self.sprite._set_center_y((value + 0.5)*self.env_height / self.mat_rows)

    def on_draw(self):
        self.sprite.draw()

class SpriteEnvironmentObject(SpriteMatrixObject, ABC):
    def __init__(self, pos_x, pos_y, environment, url, reward, reset = False):
        super().__init__(pos_x, pos_y, environment, url)
        self.reward = reward
        self.reset = reset
        self.environment.add_object(self)
    
    @property
    def id(self) -> int:
        return self.pos_x * ( self.mat_rows ) + self.pos_y

class Blank(MatrixBasedGameObject):
    def __init__(self, pos_x, pos_y, environment):
        super().__init__(pos_x, pos_y, environment)
        self.reward = -1
        self.reset = False
        
    @property
    def id(self) -> int:
        return self.pos_x * ( self.mat_rows ) + self.pos_y
    
    @property
    def pos_x(self) -> int:
        return self._pos_x
    
    @pos_x.setter
    def pos_x(self, value : int):
        self._pos_x = value

    @property
    def pos_y(self) -> int:
        return self._pos_y
    
    @pos_y.setter
    def pos_y(self, value : int):
        self._pos_y = value


class Start(SpriteEnvironmentObject):
    def __init__(self, pos_x, pos_y, environment):
        super().__init__(pos_x, pos_y, environment, 'Start.png', -1)

class Candy(SpriteEnvironmentObject):
    def __init__(self, pos_x, pos_y, environment):
        super().__init__(pos_x, pos_y, environment, 'Candy.png', 5)

class Poison(SpriteEnvironmentObject):
    def __init__(self, pos_x, pos_y, environment):
        super().__init__(pos_x, pos_y, environment, 'Poison.png', -5)

class Death(SpriteEnvironmentObject):
    def __init__(self, pos_x, pos_y, environment):
        super().__init__(pos_x, pos_y, environment, 'Death.png', -50, True)

class Success(SpriteEnvironmentObject):
    def __init__(self, pos_x, pos_y, environment):
        super().__init__(pos_x, pos_y, environment, 'Success.png', 100, True)
        

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

