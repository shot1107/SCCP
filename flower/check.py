from keras.models import Sequential
from keras.layers import Activation, Dense
from PIL import Image
import numpy as np, sys
# 変数の宣言
classes = 3
photo_size = 75
data_size = photo_size * photo_size * 3
labels = ["桜", "ヒマワリ", "バラ"]

# モデルを構築
def build_model():
  # モデルを定義 --- (1)
  model = Sequential()
  model.add(Dense(units=64, input_dim=(data_size)))
  model.add(Activation('relu'))
  model.add(Dense(units=classes))
  model.add(Activation('softmax'))
  model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy'])
  # 学習済みモデルの重みのデータを読み込み --- (2)
  model.load_weights('flower.hdf5')
  return model

# 画像を判定する
def check(model, fname):
  # 画像を読み込み正規化する --- (3)
  img = Image.open(fname)
  img = img.convert('RGB')
  img = img.resize((photo_size, photo_size))
  data = np.asarray(img).reshape((-1, data_size)) / 256
  # どの花の画像か推測する --- (4)
  res = model.predict([data])[0]
  y = res.argmax() # 値の中で最も値が大きいものが答え --- (5)
  per = int(res[y] * 100) # --- 正解率を求める
  print("{0} ({1} %)".format(labels[y], per))

if len(sys.argv) <= 1:
  print('check.py ファイル名')
  quit()

model = build_model()
check(model, sys.argv[1])

