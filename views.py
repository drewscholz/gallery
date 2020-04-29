# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import Http404

from geodude.settings import STATIC_ROOT

import base64
import os
import io
import time
import numpy as np
import cv2

def directory(request):
    encoded_imgs = get_encoded_images(resize_x=100, resize_y=100)

    context = {"images" : encoded_imgs}
    return render(request, 'gallery.html', context)

def select(request, *args, **kwargs):
    selected_img = kwargs.get('img')

    encoded_imgs = get_encoded_images()

    context = {'images' : encoded_imgs, 'selected_img': selected_img}
    return render(request, 'carousel.html', context)


def get_encoded_images(resize_x=None, resize_y=None):
    image_dir = STATIC_ROOT + "/img/"

    files = os.listdir(image_dir)

    # filter images by file extenstion
    imgs = [file for file in files if file.endswith('jpg')]

    # sort images by file name
    imgs = sorted(imgs)

    encoded_imgs = []

    for img in imgs:
        image = cv2.imread(image_dir + img)

        if resize_x and resize_y:
            # resize image
            resized = cv2.resize(image, (resize_x, resize_y))
        else:
            # downsize image for full screen
            (h, w) = image.shape[:2]
            if h > w :
                dim = (900, 1440)
            else:
                dim = (1440, 900)

            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        buffer = cv2.imencode('.jpg', resized)[1] # convert to numpy array
        b64 = base64.b64encode(buffer).decode('ascii') # convert to base64

        encoded_imgs.append(
            dict(
                thumbnail=b64,
                name=img
            )
        )

    return encoded_imgs
