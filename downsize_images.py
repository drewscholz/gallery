# run this script once to downsize your images so they will load faster for the gallery app

import cv2
import os

new_height = 900
new_width = 1440

image_dir = "path_to_images"

files = os.listdir(image_dir)

# filter images by file extension
imgs = [file for file in files if file.endswith('jpg')]

for img in imgs:
    print("img: ", img)
    image = cv2.imread(image_dir + img)
    (h, w) = image.shape[:2]
    if h > w :
        dim = (new_height, new_width)
    else:
        dim = (new_width, new_height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("s"+img, resized) 
