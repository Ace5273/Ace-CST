from help_classes.keyboard import BotKeyboard, BaseBotKeyboard
from help_classes.base_game import GameObject
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
    
    def decide_on_action(self):

        self.keyboard.release_all()

        if random.uniform(0, 1) < self.exploration_rate:
            self.exploration_rate *= self.exploration_decay_rate
            self.keyboard.press_key_by_index(random.randint(0, len(self.keyboard) - 1))
        # else:
        #     np.argmax(q_table[state])
    


class Enviroment(GameObject):
    def __init__(self):
        self.Ai = QAi(BaseBotKeyboard, [])

