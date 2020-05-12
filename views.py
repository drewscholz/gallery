# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from geodude.settings import STATIC_ROOT

import base64
import os
import io
import time
import numpy as np
import cv2
import math


class ImageState():
    TOTAL_IMG_NUM = 0
    IMAGES = []
    CURRENT_PAGE = 1
    IMAGES_PER_PAGE = 6

img_state = ImageState()


def directory(request):
    img_state.CURRENT_PAGE = 1

    encoded_imgs = get_encoded_images()

    pages = range(1, math.ceil(img_state.TOTAL_IMG_NUM/img_state.IMAGES_PER_PAGE)+1)

    context = {"images" : encoded_imgs, "pages": pages, "current_page": img_state.CURRENT_PAGE}

    return render(request, 'gallery.html', context)


def page(request, *args, **kwargs):

    selected_page = kwargs.get('page')

    if selected_page == 'prev':
        img_state.CURRENT_PAGE -= 1
    elif selected_page == 'next':
        img_state.CURRENT_PAGE += 1
    else:
        img_state.CURRENT_PAGE = int(selected_page)

    encoded_imgs = get_encoded_images()

    pages = range(1, math.ceil(img_state.TOTAL_IMG_NUM/img_state.IMAGES_PER_PAGE)+1)

    context = {"images" : encoded_imgs, "pages": pages, "current_page": img_state.CURRENT_PAGE}

    return render(request, 'gallery.html', context)


def select(request, *args, **kwargs):
    selected_img = kwargs.get('img')

    if len(img_state.IMAGES) == 0:
        encoded_imgs = get_encoded_images()
    else:
        encoded_imgs = img_state.IMAGES

    context = {'images' : encoded_imgs, 'selected_img': selected_img}
    return render(request, 'carousel.html', context)



def get_encoded_images(resize_x=None, resize_y=None):
    #image_dir = "/var/www/html/geodude/gallery/static/img/"
    image_dir = '/Users/Drew/drew/geodude/geodude/gallery/static/img/'
    files = os.listdir(image_dir)

    # filter images by file extenstion
    imgs = [file for file in files if file.endswith('jpg')]

    # sort images by file name
    imgs = sorted(imgs)
    img_state.TOTAL_IMG_NUM = len(imgs)

    # filter by page
    imgs = imgs[(img_state.CURRENT_PAGE-1)*img_state.IMAGES_PER_PAGE:img_state.CURRENT_PAGE*img_state.IMAGES_PER_PAGE]

    encoded_imgs = []

    for img in imgs:
        with open(image_dir+img, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')

        encoded_imgs.append(
            dict(
                thumbnail=b64,
                name=img
            )
        )

    img_state.IMAGES = encoded_imgs
    return encoded_imgs
