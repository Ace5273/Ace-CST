from help_classes.keyboard import BotKeyboard, BaseBotKeyboard , ArrowKeyboard
from help_classes.base_game import GameObject
from game_objects import PlayerMatrixObject
from arcade.draw_commands import draw_line, draw_circle_filled
from arcade.color import BLACK, GREEN, RED, BLUE, METALLIC_SUNBURST
from enum import Enum
import random
import numpy as np 

class QAi(PlayerMatrixObject):

    def __init__(self,pos_x, pos_y, enviroment, url, keyboard, game_objects, learning_rate = 0.01, \
                    discount_rate = 0.95, exploration_rate = 0.9, exploration_decay_rate = 0.95):
        super().__init__(pos_x, pos_y, enviroment, url, keyboard)
        self.game_objects = game_objects
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.Qlearning_Table = np.zeros((len(keyboard),len(game_objects)))
    
    def update_q_table(self, action, old_state, new_state):

        current_q_value = self.Qlearning_Table[action][old_state]
        reward          = self.game_objects[new_state]
        future_reward   = self.discount_rate * np.max(self.Qlearning_Table[:][new_state])

        self.Qlearning_Table[action, old_state] = current_q_value + self.learning_rate * (
                            reward + 
                            future_reward -
                            current_q_value
            )
    
    def decide_on_action(self, curr_state):

        self.keyboard.release_all()

        if random.uniform(0, 1) <= self.exploration_rate:
            # Imma explore the area
            self.exploration_rate *= self.exploration_decay_rate
            self.keyboard.press_key_by_index(random.randint(0, self.keyboard.get_amount_of_keys() - 1))
        else:
            # Imma exploit the area
            best_key = np.argmax(self.Qlearning_Table[:][curr_state])
            self.keyboard.press_key_by_index(best_key)

class Enviroment(GameObject):
    def __init__(self, width, height, rows = 5, cols = 4):
        super().__init__()

        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols

        self.obj_locations = np.zeros((rows, cols), int)
        self.lines = []

        self.build_line_array(width,height,cols,rows)
        self.define_enviroment()
        
        self.Baby = QAi(0,0,self,'baby.png', ArrowKeyboard, self.enviroment_objects_rewards())

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
    
    def enviroment_objects_rewards(self):
        return [-1, 0, -1,5,10,10]

    def define_enviroment(self):

        for row in range(self.rows):
            for col in range(self.cols):
                self.obj_locations[row][col] = 0

        self.obj_locations[0][0] = 1
        self.obj_locations[1][1] = 2
        self.obj_locations[3][1] = 3
        self.obj_locations[3][3] = 4

    #def on_update(self,delta_time):

    #    curr_state = self.enviroment[self.AI.pos_x][self.AI.pos_y]

    #    self.AI.decide_on_action(curr_state)
    #    self.AI.update()

    #    new_state = self.enviroment[self.AI.pos_x][self.AI.pos_y]

    #    self.AI.update_q_table(self.AI.action, curr_state, new_state)

    #    pass
    
    def on_draw(self):
        for line in self.lines:
            draw_line(line[0],line[1],line[2],line[3],BLACK,5)
        
        #for row in range(self.rows):
        #    for col in range(self.cols):

        #        curr_enviroment_object = self.enviroment[row][col]
        #        center_x = (row + 0.5) * self.width/self.cols
        #        center_y = (col + 0.5) * self.height/self.rows

        #        if curr_enviroment_object == 2:
        #            draw_circle_filled(center_x, center_y, \
        #                min(self.width, self.height)/(max(self.rows,self.cols)*2), BLACK)

        #        if curr_enviroment_object == 1:
        #            draw_circle_filled(center_x, center_y, \
        #                min(self.width, self.height)/(max(self.rows,self.cols)*2), GREEN)
                
        #        if curr_enviroment_object == 3:
        #            draw_circle_filled(center_x, center_y, \
        #                min(self.width, self.height)/(max(self.rows,self.cols)*2), RED)
                
        #        if curr_enviroment_object == 4:
        #            draw_circle_filled(center_x, center_y, \
        #                min(self.width, self.height)/(max(self.rows,self.cols)*2), BLUE)
        
        #self.AI.draw()

