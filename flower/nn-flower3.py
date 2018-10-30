from keras.models import Sequential
from keras.layers import Activation, Dense
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

classes = 3 
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
  X = np.reshape(X, (-1, data_size))
  X_test = np.reshape(X_test, (-1, data_size))
  model = train(X, y)
  model_eval(model, X_test, y_test)

def train(X, y):
  model = Sequential()
  model.add(Dense(units=64, input_dim=(data_size)))
  model.add(Activation('relu'))
  model.add(Dense(units=classes))
  model.add(Activation('softmax'))
  model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy'])
  model.fit(X, y, epochs=30)
  model.save_weights("flower.hdf5")
  return model

def model_eval(model, X, y):
  score = model.evaluate(X, y)
  print('loss=', score[0])
  print('accuracy=', score[1])
  
if __name__ == "__main__":
  main()

