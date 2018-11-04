from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D
from keras.optimizers import Adam

from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.utils import plot_model
from keras.callbacks import TensorBoard

from keras.datasets import cifar10
from keras.utils import np_utils
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import keras
print(keras.__version__)
classes = 2 
data_size = 75 * 75 * 3 

def main():
  # 学習データの読み込み 
  data = np.load("./photo-min2.npz")
  X = data["X"]
  y = data["y"]
  # テストデータの読み込み
  data = np.load("./photo-test.npz")
  X_test = data["X"]
  y_test = data["y"]
  X = np.reshape(X, (-1, 75, 75, 3))
  X_test = np.reshape(X_test, (-1, data_size))
  y = np_utils.to_categorical(y, 2)
  y_test = np_utils.to_categorical(y_test, 2)  
  model = train(X, y)
  model_eval(model, X_test, y_test)

def train(X, y):
  model = Sequential()
  '''
  model.add(Dense(units=64, input_dim=(data_size)))
  model.add(Activation('relu'))
  model.add(Dense(units=classes))
  model.add(Activation('softmax'))
  model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy'])
  model.fit(X, y, epochs=30)
  '''
  model.add(Conv2D(75,3,input_shape=(75, 75, 3)))  
  model.add(Activation('relu'))
  model.add(Conv2D(75,3))
  model.add(Activation('relu'))
  model.add(MaxPool2D(pool_size=(2,2)))

  model.add(Conv2D(150,3))
  model.add(Activation('relu'))
  model.add(MaxPool2D(pool_size=(2,2)))

  model.add(Flatten())
  model.add(Dense(64))
  model.add(Activation('relu'))
  model.add(Dropout(1.0))

  model.add(Dense(2, activation='softmax'))

  adam = Adam(lr=1e-4)

  model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=["accuracy"])

  model.fit(X, y, batch_size=1, epochs=3, validation_split=0.1)
  
  model.save_weights("flower.hdf5")
  return model

def model_eval(model, X, y):
  score = model.evaluate(X, y)
  print('loss=', score[0])
  print('accuracy=', score[1])
  
if __name__ == "__main__":
  main()

