from PIL import Image
import os

base_dir = os.path.dirname(__file__)
path_img = os.path.join(base_dir, 'img', '1.png')
img = Image.open(path_img)

print(img.size)
w, h = img.size
img_small = img.resize((round(w*0.5), round(h*0.5)))
print(img_small.size)

print(int(26.5))

