from torchvision import transforms
from PIL import Image
import os

transform = transforms.Compose([
    transforms.RandomRotation(40),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    transforms.ToTensor()
])

dir = "ds/big_ds"
dest = "c_aug"

if not os.path.exists(dest):
    os.makedirs(dest)

images = os.listdir(dir)
n = len(images)

i = 1

for image in images:
    img = Image.open(f"{dir}/{image}")
    img_transformed = transform(img)
    img_transformed_pil = transforms.ToPILImage()(img_transformed)
    img_transformed_pil.save(f'{dest}/aug_{image}')

    print(f"{n - i} left")
    i += 1