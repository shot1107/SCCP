import sys, os, keras
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import Callback, CSVLogger

epochs = 30 
batch_size = 128

def plot_result(history):
    # accuracy
    plt.figure()
    plt.plot(history.history['acc'], label='acc', marker='.')
    plt.plot(history.history['val_acc'], label='val_acc', marker='.')
    plt.grid()
    plt.legend(loc='best')
    plt.title('accuracy')
    plt.savefig('graph_accuracy.png')
    plt.show()

    # loss
    plt.figure()
    plt.plot(history.history['loss'], label='loss', marker='.')
    plt.plot(history.history['val_loss'], label='val_loss', marker='.')
    plt.grid()
    plt.legend(loc='best')
    plt.title('loss')
    plt.savefig('graph_loss.png')
    plt.show()

def main(input):
    input_dir = 'image_data'
    nb_classes = len([name for name in os.listdir(input_dir)])
    if input == False :
        x_train, x_test, y_train, y_test = np.load("./face.npy")
        # データを正規化する
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255

        y_train = np_utils.to_categorical(y_train, nb_classes)
        y_test = np_utils.to_categorical(y_test, nb_classes)
    #モデルの作成
    model = Sequential()
    if input == False : 
        model.add(Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]))
    else : 
        model.add(Conv2D(32, (3, 3), padding='same', input_shape=input))
    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(Activation('relu'))
    #model.add(Conv2D(32, (3, 3)))
    #model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    #model.add(Conv2D(64, (3, 3)))
    #model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten()) 
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.summary()

    # 学習してモデルを保存
    if input == False :
        history = model.fit(x_train, y_train,
                            batch_size=batch_size, epochs=epochs,
                            validation_split=0.1)

        hdf5_file = "./model/face-model.hdf5"

        model.save_weights(hdf5_file)

        score = model.evaluate(x_test, y_test)
        print('loss: {0}'.format(score[0]))
        print('accuracy: {0}'.format(score[1]))
        plot_result(history)

    return model

if __name__ == "__main__":
    history = main(False)
