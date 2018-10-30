# 画像をnumpy形式に変換(回転操作で増量作成)
import numpy as np
from PIL import Image
import os, glob, random
# 変数の初期化
photo_size = 75 # 画像サイズ
X = [] # 画像データ
y = [] # ラベルデータ
used_file = {} # データセットをユニークにするため

# path以下の画像を最大max_photoだけ読む 
def glob_images2(path, label, max_photo, rotate):
  files = glob.glob(path + "/*.jpg")
  random.shuffle(files) 
  # 各ファイルを処理
  i = 0
  for f in files:
    if i >= max_photo: break
    if f in used_file: continue # 同じファイルを使わない
    used_file[f] = True
    i += 1
    # 画像ファイルを読む
    img = Image.open(f)
    img = img.convert("RGB") # 色空間をRGBに
    img = img.resize((photo_size, photo_size))
    X.append(image_to_data(img))
    y.append(label)
    if not rotate: continue
    # 角度を少しずつ変えた画像を追加 --- (1)
    for angle in range(-20, 21, 5):
      # 角度を変更
      if angle != 0:
        img_angle = img.rotate(angle)
        X.append(image_to_data(img_angle))
        y.append(label)
      # 反転
      img_r = img_angle.transpose(Image.FLIP_LEFT_RIGHT)
      X.append(image_to_data(img_r))
      y.append(label)

def image_to_data(img): # 画像データを正規化
  data = np.asarray(img)
  data = data / 256
  data = data.reshape(photo_size, photo_size, 3)
  return data

# 最大枚数max_photoのデータセットを作る
def make_dataset2(max_photo, outfile, rotate):
  global X
  global y
  X = []
  y = []
  # 各画像のフォルダを読む
  glob_images2("./sakura-ok", 0, max_photo, rotate)
  glob_images2("./sunflower-ok", 1, max_photo, rotate)
  glob_images2("./rose-ok", 2, max_photo, rotate) 
  X = np.array(X, dtype=np.float32)
  np.savez(outfile, X=X, y=y)
  print("saved:" + outfile)

# データセットを作成する
make_dataset2(100, "photo-min2.npz", rotate=True)
make_dataset2(100, "photo-test.npz", rotate=False)

