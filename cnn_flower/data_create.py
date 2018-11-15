from PIL import Image
import sys
import os, glob
import numpy as np
import random, math

image_size = 50 
# トレーニングデータを生成
class DataCreate : 
  def __init__(self, script_name):
    Image.LOAD_TRUNCATED_IMAGES = True

  def create(self) :
    input_dir = "image_data"
    categorys = []

    dir_list = os.listdir(input_dir)
    for index, dir_name in enumerate(dir_list):
      categorys.append(dir_name)
    train_data = [] # 画像データ, ラベルデータ
    for idx, category in enumerate(categorys): 
        try:
            print("---", category)
            image_dir = input_dir + "/" + category
            files = glob.glob(image_dir + "/*.jpg")
            for i, f in enumerate(files):
                img = Image.open(f)
                img = img.convert("RGB")
                img = img.resize((image_size, image_size))
                data = np.asarray(img)
                train_data.append([data, idx])
                 
                for angle in range(-20, 21, 5):
                    if angle != 0:
                        img_angle = img.rotate(angle)
                        train_data.append([image_to_data(img_angle), idx])
                    img_reverse = img_angle.transpose(Image.FLIP_LEFT_RIGHT)
                    train_data.append([image_to_data(img_reverse), idx])
                
                if i == 300 :
                    print("Next")
                    break;
                    
        except:
            print("SKIP : " + category)
    print(len(train_data))
    # データをshuffle
    random.shuffle(train_data)
    X, Y = [],[]
    for data in train_data: 
      X.append(data[0])
      Y.append(data[1])
    test_idx = math.floor(len(X) * 0.8)
    xy = (np.array(X[0:test_idx]), np.array(X[test_idx:]), 
          np.array(Y[0:test_idx]), np.array(Y[test_idx:]))
    np.save("./face.npy", xy)

def image_to_data(img):
    data = np.asarray(img) / 255
    data = data.reshape(image_size, image_size, 3)

    return data

if __name__ == "__main__":
  args = sys.argv
  datacreate = DataCreate(args[0])
  datacreate.create()
