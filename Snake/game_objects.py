from help_classes.base_game import GameObject
from help_classes.keyboard import BotKeyboard, BaseKeyboard, ArrowKeyboard
from arcade.draw_commands import load_texture, draw_texture_rectangle, draw_rectangle_filled
from help_classes.content_manager import LoadSprite, Sprite
from abc import ABC, abstractmethod
from arcade.color import GREEN, RED
import random

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

class BaseSnake(MatrixBasedGameObject):

    movemenet_vectors = [[1,0],[0,1],[-1,0],[0,-1]]


    def __init__(self, environment, keyboard: BaseKeyboard, color = GREEN):
        self.snake_parts = [[0,0]]
        super().__init__(environment.cols/2, environment.rows/2, environment)

        self.keyboard = keyboard
        self.color = color
        self.apple = [random.randint(0, self.mat_cols), random.randint(0, self.mat_rows)]

        self.curr_vec_movement = 0
    
    def reset_snake(self):
        self.snake_parts = [self.snake_parts[-1]]
        self.pos_x = self.mat_cols / 2
        self.pos_y = self.mat_rows / 2
    
    def self_eaten(self):

        if len(self.snake_parts) <= 2:
            return False

        for part in self.snake_parts[:-1]:
            if part[0] == self.snake_parts[-1][0] and part[1] == self.snake_parts[-1][1]:
                return True
        return False
    
    def on_update(self, delta_time):

        self.set_vec_movement()
        self.move_snake()

        if(self.self_eaten()):
            self.reset_snake()
            return
        
        if self.pos_x < 0 or \
            self.pos_x >= self.mat_cols or \
            self.pos_y < 0 or \
            self.pos_y >= self.mat_rows:

            self.reset_snake()
            return

        if self.pos_x == self.apple[0] and \
            self.pos_y == self.apple[1]:
            self.add_part_to_snake()
            self.generate_apple()

    def set_vec_movement(self):
        if self.keyboard.is_key_pressing('right'):
            self.curr_vec_movement = 0
        elif self.keyboard.is_key_pressing('up'):
            self.curr_vec_movement = 1
        elif self.keyboard.is_key_pressing('left'):
            self.curr_vec_movement = 2
        elif self.keyboard.is_key_pressing('down'):
            self.curr_vec_movement = 3
    
    def move_snake(self):
        for i in range(0, len(self.snake_parts) - 1, 1):

            self.snake_parts[i][0] = self.snake_parts[i+1][0]
            self.snake_parts[i][1] = self.snake_parts[i+1][1]

        self.pos_x += self.movemenet_vectors[self.curr_vec_movement][0]
        self.pos_y += self.movemenet_vectors[self.curr_vec_movement][1]
    
    def add_part_to_snake(self):
        self.snake_parts.insert(0,[self.snake_parts[0][0], self.snake_parts[0][1]])
    
    def generate_apple(self):

        while True:

            self.apple = [random.randint(0, self.mat_cols - 1), random.randint(0, self.mat_rows - 1)]
            
            genreted_on_snake = False

            for part in self.snake_parts:
                if part[0] == self.apple[0] and part[1] == self.apple[1]:
                    genreted_on_snake = True
                    break
            
            if not genreted_on_snake:
                return
    
    def on_draw(self):

        self.draw_rectangle(self.apple[0], self.apple[1], RED)

        for part in self.snake_parts:
            self.draw_snake_bit(part[0], part[1])

        self.draw_snake_bit(self.pos_x,self.pos_y)
    
    def draw_snake_bit(self, pos_x, pos_y):
        self.draw_rectangle(pos_x,pos_y,self.color)
    
    def draw_rectangle(self, pos_x, pos_y, color):
        draw_rectangle_filled(  (((pos_x + 0.5)) * (self.env_height) / (self.mat_rows) ),
                                (((pos_y + 0.5)) * (self.env_height) / (self.mat_rows) ),
                                (self.env_width) / self.mat_cols,
                                self.env_height / self.mat_rows,
                                color)

    @property
    def pos_x(self) -> int:
        return self.snake_parts[-1][0]
    
    @pos_x.setter
    def pos_x(self, value : int):
        self.snake_parts[-1][0] = value

    @property
    def pos_y(self) -> int:
        return self.snake_parts[-1][1]
    
    @pos_y.setter
    def pos_y(self, value : int):
        self.snake_parts[-1][1] = value

class SnakePlayer(BaseSnake):

    def __init__(self,environment):
        super().__init__(environment, ArrowKeyboard)