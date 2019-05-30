import random
import gym
import numpy as np
from collections import deque
import tensorflow as tf
import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

EPISODES = 5000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    # This is the q learning function that calculate loss
    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond  = tf.keras.backend.abs(error) <= clip_delta

        squared_loss = 0.5 * tf.keras.backend.square(error)
        quadratic_loss = 0.5 * tf.keras.backend.square(clip_delta) + clip_delta * (tf.keras.backend.abs(error) - clip_delta)

        return tf.keras.backend.mean(tf.where(cond, squared_loss, quadratic_loss))

    def _build_model(self):

        # Neural Net for Deep-Q learning Model
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss=self._huber_loss,
                      optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    # only ment for replay
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        
        # We need to explore therefor
        # we have epsilon and if a random number
        # is smaller the it.
        if np.random.rand() <= self.epsilon:
            
            # give a number from 0 to 2(not included)
            return random.randrange(self.action_size)
        
        # predict the action value
        act_values = self.model.predict(state)

        # and return the most likely action to do right now
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32

    for e in range(EPISODES):
        
        # Reset the enviroment
        state = env.reset()

        # we've changed the state from an object(?) to an array
        state = np.reshape(state, [1, state_size])

        # for 500 times
        for time in range(500):
            # env.render()

            # get either 0 or 1
            action = agent.act(state)

            # apply to the inviroment the action
            # and get the next state, the reward and if done
            next_state, reward, done, _ = env.step(action)

            # if the game is still continued then
            # give the ai the reward that he alwayes wanted
            # otherwise punish him
            reward = reward if not done else -10

            # change the state to an array
            next_state = np.reshape(next_state, [1, state_size])

            # I think this method is optional
            agent.remember(state, action, reward, next_state, done)

            # the state is the next state
            state = next_state

            # the game is done the ai lost
            if done:

                # update the target model
                agent.update_target_model()

                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, time, agent.epsilon))
                break
            
            
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        # if e % 10 == 0:
        #     agent.save("./save/cartpole-ddqn.h5")