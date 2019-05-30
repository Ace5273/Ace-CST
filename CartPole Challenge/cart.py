import arcade
import math
import numpy as np
from collections import deque
import random
from event_hook import EventHook
import os

from help_classes.base_game import GameObject
from help_classes.vector import Point
from help_classes.keyboard import BotKeyboard, BaseKeyboard
# import tensorflow as tf

class Enviroment():

    def __init__(self):
        Enviroment.gravity          = 1.2
        Enviroment.friction         = 0.001
        Enviroment.pole_length      = 200
        Enviroment.pole_mass        = 15
        Enviroment.pole_start_angle = 90
        Enviroment.cart_mass        = 20
        Enviroment.cart_position_x  = 600
        Enviroment.cart_position_y  = 200

    @staticmethod
    def get_state(cart):
        return np.array((
                # Enviroment.gravity, 
                # Enviroment.friction,
                # Enviroment.pole_length,
                # Enviroment.pole_mass,
                cart.pole.angle,
                cart.pole.ang_velocity,
                # cart.pole.ang_acc,
                # Enviroment.cart_mass,
                cart.position.x,
                cart.velocity
                # cart.accelartion
        ))

class Pole(GameObject):

    def __init__(self):
        super().__init__()
        self.length = Enviroment.pole_length
        self.size = 10
        self.mass = Enviroment.pole_mass
        self.reset()
    
    def reset(self):
        self._angle = Enviroment.pole_start_angle + random.random()
        self._ang_velocity  = 0
        self._ang_acc  = 0
        self.position = Point(Enviroment.cart_position_x,Enviroment.cart_position_y)
        self.end_of_pole = self.position + \
             Point(math.cos(self.angle) * self.length, math.sin(self.angle) * self.length)
    
    @property
    def angle(self):
        return math.radians(self._angle)
    
    @angle.setter
    def angle(self, value):
        self._angle = math.degrees(value)
    
    @property
    def ang_velocity(self):
        return math.radians(self._ang_velocity)
    
    @ang_velocity.setter
    def ang_velocity(self, value):
        self._ang_velocity = math.degrees(value)

    @property
    def ang_acc(self):
        return math.radians(self._ang_acc)
    
    @ang_acc.setter
    def ang_acc(self, value):
        self._ang_acc = math.degrees(value)

    def on_draw(self):
        self.position.draw_line(self.end_of_pole, arcade.color.BROWN_NOSE, self.size)
        self.position.draw(color= arcade.color.RED,size=10)
        self.end_of_pole.draw(color= arcade.color.RED,size=10)

class Cart(GameObject):

    def __init__(self, keyboard : BaseKeyboard):
        self.keyboard = keyboard
        self.pole = Pole()
        self.Mass = Enviroment.cart_mass
        self.force_factor = 1
        self.width = 70
        self.height = 50

        self.reset()
        super().__init__()
    
    def reset(self):
        self.accelartion = 0
        self.velocity = 0
        self.force = 0
        self.position = Point(Enviroment.cart_position_x, Enviroment.cart_position_y)
        self.pole.reset()
    
    # def round_done(self, success = False, failed = False):
    #     self.reset()
    
    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height, arcade.color.SILVER)
    
    def on_update(self, delta_time):
        
        if (self.keyboard.is_key_pressed_down('left') ^ self.keyboard.is_key_pressed_down('right')):

            if self.keyboard.is_key_pressed_down('left'):
                self.force = -self.Mass * self.force_factor
            
            elif self.keyboard.is_key_pressed_down('right'):
                self.force = self.Mass * self.force_factor

            else:
                self.force = 0
        
        else:
            self.force = 0

        self.pole.ang_acc = (self.Mass + self.pole.mass) * \
                            (Enviroment.gravity * math.sin(self.pole.angle - math.radians(90)) - Enviroment.friction * self.pole.ang_velocity)

        self.pole.ang_acc -= (self.pole.length * self.pole.mass * \
                                self.pole.ang_velocity ** 2 * \
                                math.sin(self.pole.angle - math.radians(90)) + self.force) * math.cos(self.pole.angle - math.radians(90))
        
        self.pole.ang_acc /= self.pole.length * (self.Mass + (1 - math.cos(self.pole.angle - math.radians(90)) ** 2) * self.pole.mass)

        self.accelartion = -self.pole.mass * Enviroment.gravity * math.sin(self.pole.angle - math.radians(90)) * math.cos(self.pole.angle - math.radians(90))
        self.accelartion += self.pole.mass * self.pole.length * self.pole.ang_velocity ** 2 * math.sin(self.pole.angle - math.radians(90))
        self.accelartion += Enviroment.friction * self.pole.mass * self.pole.ang_velocity * math.cos(self.pole.angle - math.radians(90))
        self.accelartion += self.force
        self.accelartion /= self.Mass + (1 - math.cos(self.pole.angle - math.radians(90))**2) * self.pole.mass

        self.velocity += self.accelartion
        self.position.x += self.velocity
        self.pole.position.x = self.position.x

        self.pole.ang_velocity += self.pole.ang_acc
        self.pole.angle += self.pole.ang_velocity
        self.pole.end_of_pole = self.position + \
             Point(math.cos(self.pole.angle) * self.pole.length, math.sin(self.pole.angle) * self.pole.length)

class BotCart(Cart):
    def __init__(self):
        super().__init__(BotKeyboard(left = False, right = False))
        self.keyboard : BotKeyboard


    def on_update(self, delta_time):
        super().on_update(delta_time)

        main_act = ''

        self.keyboard.release_key('left')
        self.keyboard.release_key('right')

        if self.pole.angle < math.radians(90) and self.pole.ang_velocity < 0:
            main_act = 'left'
        elif self.pole.angle > math.radians(90) and self.pole.ang_velocity > 0:
            main_act = 'right'
        
        if main_act != '':
            self.keyboard.press_key(main_act)

# class AICart(Cart):
#     def __init__(self):
#         super().__init__(BotKeyboard(left = False, right = False))
#         self.keyboard : BotKeyboard
#         self.gamma = 0.95    # discount rate
#         self.epsilon = 1.0  # exploration rate
#         self.epsilon_min = 0.01
#         self.epsilon_decay = 0.9999
#         self.learning_rate = 0.001
#         self.memory = deque(maxlen=2000)
#         self.batch_size = 32
#         self.model = self._build_model()
#         self.target_model = self._build_model()
#         self.update_target_model()
#         self.update_num = 0
#         self.end_update = 500
#         self.episode = 1
#         # self.episodes = 5000

#     def update_target_model(self):
#         # copy weights from model to target_model
#         self.target_model.set_weights(self.model.get_weights())
    
#     def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
#         error = y_true - y_pred
#         cond  = tf.keras.backend.abs(error) <= clip_delta

#         squared_loss = 0.5 * tf.keras.backend.square(error)
#         quadratic_loss = 0.5 * tf.keras.backend.square(clip_delta) + clip_delta * (tf.keras.backend.abs(error) - clip_delta)

#         return tf.keras.backend.mean(tf.where(cond, squared_loss, quadratic_loss))
    
#     def _build_model(self):
#         """
#         This function builds the model
#         """
#         model = tf.keras.models.Sequential()
#         model.add(tf.keras.layers.Dense(24, input_dim= len(Enviroment.get_state(self)), activation='relu'))
#         model.add(tf.keras.layers.Dense(24, activation='relu'))
#         model.add(tf.keras.layers.Dense(self.keyboard.get_amount_of_keys(), activation='linear'))
#         model.compile(loss=self._huber_loss,
#                       optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
#         return model
    
#     def act(self, state):
#         """
#         This function decide what action
#         should the ai use
#         """
#         act_num = None
        
#         # We need to explore therefor
#         # we have epsilon and if a random number
#         # is smaller the it.
#         if np.random.rand() <= self.epsilon:
            
#             # give a number from 0 to 2(not included)
#             act_num = random.randrange(self.keyboard.get_amount_of_keys())
        
#         else:
#             # predict the action value
#             act_values = self.model.predict(state)

#             # and return the most likely action to do right now
#             act_num =  np.argmax(act_values[0])  # returns action
        
#         return 'left' if act_num == 0 else 'right'
    
#     # only ment for replay
#     def remember(self, state, action, reward, next_state, done):
#         """
#         place the state action reward at the memort
#         """
#         self.memory.append((state.reshape(1,4), 0 if action == 'left' else 1
#                             , reward, next_state, done))
    
#     def replay(self, batch_size):
#         """
#         This method is used to train the target model
#         so the ai will make better decisions
#         """
        
#         # Get a random sample from the memory
#         minibatch = random.sample(self.memory, batch_size)

#         # Run through each sample at the minibatch
#         for state, action, reward, next_state, done in minibatch:
#             # state = np.reshape(state,[1,4])
#             # print(state.ndim)
#             # Get the model to predict the action
#             target = self.model.predict(state)

#             # if the state is done
#             if done:

#                 # give the ai it's reward
#                 target[0][action] = reward
#             else:

#                 # get the array of predictions
#                 t = self.target_model.predict(next_state)[0]
#                 target[0][action] = reward + self.gamma * np.amax(t)

#             # train the model with the new target for a given state
#             self.model.fit(state, target, epochs=1, verbose=0)
        
#         # let the exploration rate to go down
#         if self.epsilon > self.epsilon_min:
#             self.epsilon *= self.epsilon_decay
    
#     def on_update(self, delta_time):

#         did_lose = False

#         # reset the enviroment because you won!
#         if(self.update_num == self.end_update):
#             self.round_done(success= True)
#             return

#         # Release both keys
#         self.keyboard.release_key('left')
#         self.keyboard.release_key('right')

#         # Get the action from the enviroment
#         old_state = np.reshape(Enviroment.get_state(self),[1,4])
#         action = self.act(old_state)

#         # Press the action with the key
#         self.keyboard.press_key(action)

#         # get the next state
#         super().on_update(delta_time)

#         # reset the enviroment because you lost
#         if self.pole.angle < 0 or self.pole.angle > math.radians(180):
#             did_lose = True

#         # Never forget
#         self.remember(old_state, action, 1 if not did_lose else -10
#                                 , np.reshape(Enviroment.get_state(self),[1,4]), did_lose)

#         # did the ai lost
#         if did_lose:
#             self.round_done(failed=True)
#             return
        
#         if len(self.memory) > self.batch_size:
#             self.replay(self.batch_size)

#         # Add 1 to the update number
#         self.update_num += 1
    
#     def round_done(self, success = False, failed = False):
#         """
#         Was the round ended with success
#         """
#         if success:
#             pass
#         elif failed:
#             # update the target model
#             self.update_target_model()
#             pass

#         print("episode: {}, score: {}, e: {:.2}"
#                 .format(self.episode, self.update_num, self.epsilon))
        
#         super().reset()

#         self.update_num = 0
#         self.episode += 1

#         if self.episode % 10:
#             self.save("Nim.h5")

    
#     def load(self, name):
#         """
#         Load weights of the model from a file
#         """
#         self.model.load_weights(name)

#     def save(self, name):
#         """
#         save the weights of the model to a file
#         """
#         self.model.save_weights(name)

