#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def get_pixel(src, y, x):
    if (y < 0):
        y = 0
    elif (y > (src.shape[0] - 1)):
        y = (src.shape[0] - 1)

    if (x < 0):
        x = 0
    elif (x > (src.shape[1] - 1)):
        x = (src.shape[1] - 1)

    return src[y][x]

# 最邻近缩放算法
def resize_nearest(src, dsize):
    des = np.empty(dsize+(3,), dtype=np.uint8)
    map_y = np.empty(dsize[0], dtype=np.uint16)
    map_x = np.empty(dsize[1], dtype=np.uint16)

    for i in range(0, dsize[0]):
        map_y[i] = round((i + 0.5) * src.shape[0] / dsize[0] - 0.5)

    for i in range(0, dsize[1]):
        map_x[i] = round((i + 0.5) * src.shape[1] / dsize[1] - 0.5)

    for y in range(0, dsize[0]):
        for x in range(0, dsize[1]):
            des[y][x] = src[map_y[y]][map_x[x]]

    return des

# 线性插值法
def resize_bilinear(src, dsize):
    des = np.empty(dsize+(3,), dtype=np.uint8)
    map_y_offset = np.empty(dsize[0], dtype=np.uint16)
    map_x_offset = np.empty(dsize[1], dtype=np.uint16)
    map_y_effect = np.empty((dsize[0], 2), dtype=np.double)
    map_x_effect = np.empty((dsize[1], 2), dtype=np.double)

    for i in range(0, dsize[0]):
        map_y = (i + 0.5) * src.shape[0] / dsize[0] - 0.5
        map_y_offset[i] = int(map_y)
        map_y_effect[i][0] = map_y - map_y_offset[i]
        map_y_effect[i][1] = 1 - map_y_effect[i][0]

    for i in range(0, dsize[1]):
        map_x = (i + 0.5) * src.shape[1] / dsize[1] - 0.5
        map_x_offset[i] = int(map_x)
        map_x_effect[i][0] = map_x - map_x_offset[i]
        map_x_effect[i][1] = 1 - map_x_effect[i][0]

    for y in range(0, dsize[0]):
        for x in range(0, dsize[1]):
            liner_row1 = get_pixel(src, map_y_offset[y], map_x_offset[x]) * map_x_effect[x][0] + get_pixel(src, map_y_offset[y], map_x_offset[x]+1) * map_x_effect[x][1]
            liner_row2 = get_pixel(src, map_y_offset[y]+1, map_x_offset[x]) * map_x_effect[x][0] + get_pixel(src, map_y_offset[y]+1, map_x_offset[x]+1) * map_x_effect[x][1]
            des[y][x] = liner_row1 * map_y_effect[y][0] + liner_row2 * map_y_effect[y][1]

    return des

def func_w(x):
    a = 0.5

    x = abs(x)

    if (0 <= x <= 1):
        ret = (a + 2)*(x**3) - (a+3)*(x**2) + 1
    elif (1 <= x < 2):
        ret = a*(x**3) - 5*a*(x**2) + 8*a*x - 4*a
    else:
        ret = 0

    return ret

def resize_bicubic(src, dsize):
    des = np.empty(dsize+(3,), dtype=np.uint8)

    map_y_offset = np.empty(dsize[0], dtype=np.uint16)
    map_x_offset = np.empty(dsize[1], dtype=np.uint16)
    map_y_effect = np.empty((dsize[0], 4), dtype=np.double)
    map_x_effect = np.empty((dsize[1], 4), dtype=np.double)

    for i in range(0, dsize[0]):
        map_y = (i + 0.5) * src.shape[0] / dsize[0] - 0.5
        map_y_offset[i] = int(map_y)
        alpha = map_y - map_y_offset[i]
        map_y_effect[i][0] = func_w(-1 - alpha)
        map_y_effect[i][1] = func_w(-alpha)
        map_y_effect[i][2] = func_w(1 - alpha)
        map_y_effect[i][3] = func_w(2 - alpha)

    for i in range(0, dsize[1]):
        map_x = (i + 0.5) * src.shape[1] / dsize[1] - 0.5
        map_x_offset[i] = int(map_x)
        alpha = map_x - map_x_offset[i]
        map_x_effect[i][0] = func_w(-1 - alpha)
        map_x_effect[i][1] = func_w(-alpha)
        map_x_effect[i][2] = func_w(1 - alpha)
        map_x_effect[i][3] = func_w(2 - alpha)

    for y in range(0, dsize[0]):
        for x in range(0, dsize[1]):
            cubic_row0 = get_pixel(src, map_y_offset[y]-1, map_x_offset[x]-1) * map_x_effect[x][0] + get_pixel(src, map_y_offset[y]-1, map_x_offset[x]) * map_x_effect[x][1] + get_pixel(src, map_y_offset[y]-1, map_x_offset[x]+1) * map_x_effect[x][2] + get_pixel(src, map_y_offset[y]-1, map_x_offset[x]+2) * map_x_effect[x][3]
            cubic_row1 = get_pixel(src, map_y_offset[y], map_x_offset[x]-1) * map_x_effect[x][0] + get_pixel(src, map_y_offset[y], map_x_offset[x]) * map_x_effect[x][1] + get_pixel(src, map_y_offset[y], map_x_offset[x]+1) * map_x_effect[x][2] + get_pixel(src, map_y_offset[y], map_x_offset[x]+2) * map_x_effect[x][3]
            cubic_row2 = get_pixel(src, map_y_offset[y]+1, map_x_offset[x]-1) * map_x_effect[x][0] + get_pixel(src, map_y_offset[y]+1, map_x_offset[x]) * map_x_effect[x][1] + get_pixel(src, map_y_offset[y]+1, map_x_offset[x]+1) * map_x_effect[x][2] + get_pixel(src, map_y_offset[y]+1, map_x_offset[x]+2) * map_x_effect[x][3]
            cubic_row3 = get_pixel(src, map_y_offset[y]+2, map_x_offset[x]-1) * map_x_effect[x][0] + get_pixel(src, map_y_offset[y]+2, map_x_offset[x]) * map_x_effect[x][1] + get_pixel(src, map_y_offset[y]+2, map_x_offset[x]+1) * map_x_effect[x][2] + get_pixel(src, map_y_offset[y]+2, map_x_offset[x]+2) * map_x_effect[x][3]
            des[y][x] = cubic_row0 * map_y_effect[y][0] + cubic_row1 * map_y_effect[y][1] + cubic_row2 * map_y_effect[y][2] + cubic_row3 * map_y_effect[y][3]

    return des

img = plt.imread("C:/Users/user0/Desktop/002.jpg")
res1_img = resize_nearest(img,(1140,640))
res2_img = resize_bilinear(img,(1140,640))
res3_img = resize_bicubic(img,(1140,640))

# plt.imsave("C:/Users/user0/Desktop/001_1.bmp", res1_img)
# plt.imsave("C:/Users/user0/Desktop/001_2.bmp", res2_img)

plt.subplot(1,4,1)
plt.imshow(img)
plt.axis("off")

plt.subplot(1,4,2)
plt.imshow(res1_img)
plt.axis("off")

plt.subplot(1,4,3)
plt.imshow(res2_img)
plt.axis("off")

plt.subplot(1,4,4)
plt.imshow(res3_img)
plt.axis("off")

plt.show()
