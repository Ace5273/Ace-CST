from help_classes.keyboard import BotKeyboard, BaseBotKeyboard
from help_classes.base_game import GameObject
from arcade.draw_commands import draw_line, draw_lines
from arcade.color import BLACK
import random
import numpy as np

class QAi():

    def __init__(self, keyboard :BotKeyboard, game_objects, learning_rate = 0.01, discount_rate = 0.95, exploration_rate = 0.9, exploration_decay_rate = 0.95):
        super().__init__()
        self.keyboard = keyboard
        self.game_objects = game_objects
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.Qlearning_Table = np.zeros((len(keyboard),len(game_objects + 2)))
    
    def update_q_table(self, action, old_state, new_state):

        current_q_value = self.Qlearning_Table[action, old_state]
        reward          = self.game_objects[new_state]
        future_reward   = self.discount_rate * np.max(self.Qlearning_Table[new_state, :])

        self.Qlearning_Table[action, old_state] = current_q_value + self.learning_rate * (
                            reward + 
                            future_reward -
                            current_q_value
            )
    
    def decide_on_action(self, state):

        self.keyboard.release_all()

        if random.uniform(0, 1) < self.exploration_rate:
            # Imma explore the area
            self.exploration_rate *= self.exploration_decay_rate
            self.keyboard.press_key_by_index(random.randint(0, len(self.keyboard) - 1))
        else:
            # Imma exploit the area
            best_key = np.argmax(q_table[state])
            self.keyboard.press_key_by_index(best_key)
    


class Enviroment(GameObject):
    def __init__(self, width, height):
        super().__init__()

        cols = 4
        rows = 5
        self.enviroment = np.zeros((rows, cols))
        self.lines = []
        self.build_line_array(width,height,cols,rows)

        #self.Ai = QAi(BaseBotKeyboard, [])
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

    def define_enviroment(self):
        pass

    def on_update(self,delta_time):
        pass
    
    def on_draw(self):
        for line in self.lines:
            draw_line(line[0],line[1],line[2],line[3],BLACK,5)
        pass

