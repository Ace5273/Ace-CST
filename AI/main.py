from keras.models import Sequential
import keras.datasets.mnist as mnist
import matplotlib.pyplot as plt

model = Sequential()

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(x_train[0])