import os
import shutil
from random import shuffle
from math import ceil

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("Path Exists")

ds = "./ds/c1_labeled"
data = os.listdir(ds)
data.remove('backgrounds')
names = list(set([''.join(d.split('.')[:-1]) for d in data]))

shuffle(names)

train_split = 0.8
val_split = 1 - train_split

train_len = ceil(len(names) * train_split)

train = names[:train_len]
valid = names[train_len:]

for i in train:
    print(i)

yolov8_dataset_path = './ds/my_dataset_c1'
create_directory(yolov8_dataset_path)

splits = ["train", "valid"]
for split in splits:
    create_directory(f"{yolov8_dataset_path}/{split}")
    create_directory(f"{yolov8_dataset_path}/{split}/images")
    create_directory(f"{yolov8_dataset_path}/{split}/labels")

for name in train:
    print(f"trian: {name}")
    shutil.copy(f"{ds}/{name}.txt", f"{yolov8_dataset_path}/train/labels")
    shutil.copy(f"{ds}/{name}.jpg", f"{yolov8_dataset_path}/train/images")

for name in valid:
    print(f"valid: {name}")
    shutil.copy(f"{ds}/{name}.txt", f"{yolov8_dataset_path}/valid/labels")
    shutil.copy(f"{ds}/{name}.jpg", f"{yolov8_dataset_path}/valid/images")

backgrounds = os.listdir(f"{ds}/backgrounds")

shuffle(backgrounds)

backgrounds_train_len = ceil(0.9 * len(backgrounds))

backgrounds_train = backgrounds[:backgrounds_train_len]
backgrounds_valid = backgrounds[backgrounds_train_len:]


for background in backgrounds_train:
    shutil.copy(f"{ds}/backgrounds/{background}", f"{yolov8_dataset_path}/train/images/{background}")
    print("copied to train")

for background in backgrounds_valid:
    shutil.copy(f"{ds}/backgrounds/{background}", f"{yolov8_dataset_path}/valid/images/{background}")
    print("copied to valid")