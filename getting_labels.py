import os
import shutil

dir = "./tt"

images = os.listdir(f"{dir}/big_ds")
names = [''.join(image.split('.')[:-1]) for image in images]

for name in names:
    shutil.copy(f"{dir}/labels/{name}.txt", f"{dir}/big_ds/{name}.txt")