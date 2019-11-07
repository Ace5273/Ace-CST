from game_objects import BaseSnake
from help_classes.keyboard import BasicBotKeyboard
from keras.models  import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard

class BotSnake(BaseSnake):
    def __init__(self, environment):
        super().__init__(environment, BasicBotKeyboard)
        self.model = self.create_model()

    def create_model(self):
        model = Sequential([
            Dense(16, activation='relu', input_shape=(self.environment.rows * self.environment.cols,))
        ])

        return model