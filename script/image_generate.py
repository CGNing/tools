#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt

height = 1520
width = 720

img = np.zeros((height, width, 3), np.uint8)

# WB
# for i in range(0, height):
#     if (i % 2 == 0):
#         img[i, :] = [255, 255, 255]
#     elif (i % 2 == 1):
#         img[i, :] = [0, 0, 0]

# RGBW
for i in range(0, height):
    if (i % 4 == 0):
        img[i, :, 0] = 255
    elif (i % 4 == 1):
        img[i, :, 1] = 255
    elif (i % 4 == 2):
        img[i, :, 2] = 255
    elif (i % 4 == 3):
        img[i, :] = [255, 255, 255]

# for i in range(0, height):
#     gray = round((i + 0.5)/height * 256 - 0.5)
#     if (gray < 0): gray = 0
#     img[i, :, :] = gray

plt.imshow(img, "gray")

plt.imsave("C:/Users/user0/Desktop/003.bmp",img,cmap = "gray")
