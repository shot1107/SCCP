import train as train
import sys, os
from PIL import Image
import numpy as np
#import pandas as pd

if len(sys.argv) <= 1:
  quit()

image_size = 50
input_dir = 'image_data'
categories = [name for name in os.listdir(input_dir)]

X = []
for file_name in sys.argv[1:]:
  img = Image.open(file_name)
  img = img.convert("RGB")
  img = img.resize((image_size, image_size))
  in_data = np.asarray(img)
  X.append(in_data)

X = np.array(X)

model = train.main(X.shape[1:])
model.load_weights("./model/face-model.hdf5")

predictions = model.predict(X)

for pre in predictions:
    y = pre.argmax()
    print("種類 : ", categories[y])
