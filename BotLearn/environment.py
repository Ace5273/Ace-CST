from help_classes.keyboard import BotKeyboard, BaseBotKeyboard , ArrowKeyboard
from help_classes.base_game import GameObject
from game_objects import PlayerMatrixObject, SpriteEnvironmentObject, Start , Candy, Poison, Death, Success
from arcade.draw_commands import draw_line, draw_circle_filled
from arcade.color import BLACK, GREEN, RED, BLUE, METALLIC_SUNBURST
import random
import numpy as np 

class QAi(PlayerMatrixObject):

    def __init__(self,pos_x, pos_y, environment, url, keyboard, learning_rate = 0.01, \
                    discount_rate = 1, exploration_rate = 0.999, exploration_decay_rate = 0.99):
        super().__init__(pos_x, pos_y, environment, url, keyboard)
        self.org_pos_x = pos_x
        self.org_pos_y = pos_y
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.Qlearning_Table = np.zeros((len(keyboard),self.environment.get_objects_amount()))
        Start(pos_x, pos_y, environment)
    
    def reset(self):
        self.pos_x = self.org_pos_x
        self.pos_y = self.org_pos_y
        self.exploration_rate *= self.exploration_decay_rate

    def update_q_table(self, action, old_state, new_state):

        current_q_value = self.Qlearning_Table[action,old_state]
        reward          = self.environment.reward(self.pos_x, self.pos_y)
        future_reward   = self.discount_rate * np.max(self.Qlearning_Table[:,new_state])

        self.Qlearning_Table[action, old_state] = current_q_value + self.learning_rate * (
                            reward + 
                            future_reward -
                            current_q_value
            )
    
    def decide_on_action(self, curr_state):

        key_index = None
        rnd_value = random.uniform(0, 1)
        self.keyboard.release_all()

        if rnd_value <= self.exploration_rate:
            # Imma explore the area
            key_index = random.randint(0, len(self.keyboard) - 1)
        else:
            # Imma exploit the area
            key_index = np.argmax(self.Qlearning_Table[:,curr_state])
        
        self.keyboard.press_key_by_index(key_index)

        return key_index
    
    def on_update(self,delta_time):

       curr_state = self.environment.state(self.pos_x, self.pos_y)

       if curr_state in [4,5]:
           self.reset()
           return

       action = self.decide_on_action(curr_state)
       super().on_update(delta_time)
       new_state = self.environment.state(self.pos_x, self.pos_y)

       if curr_state == new_state:
           return

       self.update_q_table(action, curr_state, new_state)


class Enviroment(GameObject):
    def __init__(self, width, height, cols = 3, rows = 3):
        super().__init__()

        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols

        self.EnvObjectLocations = np.zeros((cols, rows), object)
        self.lines = []

        self.build_line_array(width,height,cols,rows)
        
        self.Baby = QAi(0,0,self,'Baby.png', BaseBotKeyboard)
        Candy(0,2, self)
        Poison(2,0,self)
        Death(1,1,self)
        Success(2,2,self)

    def build_line_array(self,width, height, col_num, row_num):

        for i in range(col_num + 1):
            self.lines.append([i*(width-1)/col_num, 
                               1,
                               i*(width-1)/col_num,
                               height])

        for j in range(row_num + 1):
            self.lines.append([1, 
                                j*(height-1)/row_num,
                                width,
                                j*(height-1)/row_num])

    def add_object(self, obj : SpriteEnvironmentObject):
        self.EnvObjectLocations[obj.pos_x,obj.pos_y] = obj
    
    def get_objects_amount(self):
        return 6
    
    def reward(self, pos_x : int, pos_y : int):
        curr_obj = self.EnvObjectLocations[pos_x,pos_y]
        if curr_obj == 0 or curr_obj == None:
            return -1
        return self.EnvObjectLocations[pos_x,pos_y].reward
    
    def state(self, pos_x : int, pos_y : int):
        curr_obj = self.EnvObjectLocations[pos_x,pos_y]
        if curr_obj == 0 or curr_obj == None:
            return 0
        return self.EnvObjectLocations[pos_x,pos_y].id
    
    def on_draw(self):
        for line in self.lines:
            draw_line(line[0],line[1],line[2],line[3],BLACK,5)

