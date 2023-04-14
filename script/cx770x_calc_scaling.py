#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import math

# 验证算法
def cx770x_verify_scaled():
    if (is_vertical_scale == "SCALE_CR_VSCALE_DOWN"):
        int_scaled_vertical = int(int_rx_vertical / 1.5)
    elif (is_vertical_scale == "SCALE_CR_VSCALE_UP"):
        int_scaled_vertical = int(int_rx_vertical * 1.5)
    else:
        int_scaled_vertical = int_rx_vertical

    group_line = p1 if (p1 != 0) else 256
    scaled_first_line = p2 if (p2 != 0) else 256
    scaled_every_line = p3 if (p3 != 0) else 256

    if (scale_cr_inserdrawout == "SCALE_CR_INSER_EN" and group_line > scaled_first_line):
        group_insert_line = 1 + int((group_line - scaled_first_line) / scaled_every_line)
        group_origin_line = group_line - group_insert_line
        # 计算分组不能整除输出列数时
        last_insert_line = ((int_scaled_vertical % group_origin_line) - (scaled_first_line-1)) / (scaled_every_line-1)
        last_insert_line = (1 if(last_insert_line > 0) else 0) + int(last_insert_line)
        # 最终算出输出行数
        int_actual_vertical = int(int_scaled_vertical / group_origin_line) * group_line + last_insert_line

    elif (scale_cr_inserdrawout == "SCALE_CR_DRAWOUT_EN" and group_line > scaled_first_line):
        group_drop_line = 1 + int((group_line - scaled_first_line) / scaled_every_line)
        group_origin_line = group_line + group_drop_line
        # 计算分组不能整除输出列数时
        last_drop_line = ((int_scaled_vertical % group_origin_line) - (scaled_first_line+1)) / (scaled_every_line+1)
        last_drop_line = (1 if(last_drop_line > 0) else 0) + int(last_drop_line)
        # 最终算出输出行数
        int_actual_vertical = int(int_scaled_vertical / group_origin_line) * group_line - last_drop_line
    else:
        int_actual_vertical = int_scaled_vertical

    if (int_actual_vertical != int_tx_vertical):
        print ("验证的输出高度有问题")
        print ("计算出的输出高度为:", int_actual_vertical)

if (len(sys.argv)>1):
    int_rx_vertical = int(sys.argv[1])
else:
    int_rx_vertical = int(input("输入高度(单位：像素):"))

if (len(sys.argv)>2):
    int_rx_horizontal = int(sys.argv[2])
else:
    int_rx_horizontal = int(input("输入宽度(单位：像素):"))

if (len(sys.argv)>3):
    int_tx_vertical = int(sys.argv[3])
else:
    int_tx_vertical = int(input("输出高度(单位：像素):"))

if (len(sys.argv)>4):
    int_tx_horizontal = int(sys.argv[4])
else:
    int_tx_horizontal = int(input("输出宽度(单位：像素):"))


if ((int_rx_horizontal / 1.5) == int_tx_horizontal):
    is_horizontal_scale = "SCALE_CR_HSCALE_DOWN"
elif ((int_rx_horizontal * 1.5) == int_tx_horizontal):
    is_horizontal_scale = "SCALE_CR_HSCALE_UP"
elif (int_rx_horizontal == int_tx_horizontal):
    is_horizontal_scale = "SCALE_CR_HSCALE_DIS"
else:
    print("不支持非1.5的倍数的宽度缩放")
    exit(-1)

if ((int_rx_vertical / 1.25) > int_tx_vertical):
    int_scaled_vertical = int(int_rx_vertical / 1.5)
    is_vertical_scale = "SCALE_CR_VSCALE_DOWN"
elif ((int_rx_vertical * 1.25) < int_tx_vertical):
    int_scaled_vertical = int(int_rx_vertical * 1.5)
    is_vertical_scale = "SCALE_CR_VSCALE_UP"
else:
    int_scaled_vertical = int_rx_vertical
    is_vertical_scale = "SCALE_CR_VSCALE_DIS"

group_num = math.gcd(int_scaled_vertical, int_tx_vertical)

if (int_scaled_vertical < int_tx_vertical):
    # 插行
    scale_cr_inserdrawout = "SCALE_CR_INSER_EN"
    group_line = int(int_tx_vertical / group_num)
    group_insert_line = int((int_tx_vertical - int_scaled_vertical) / group_num)

    p1 = group_line

    p2 = 0
    for i in range(0, p1):
        map_vertical = round((i + 0.5) * int_scaled_vertical / int_tx_vertical - 0.5)
        if (i == (map_vertical + 1)):
            p2 = i
            break

    p3 = int(group_line/group_insert_line)
    p3 = p3 if ((p2 + p3) <= p1) else 0

elif (int_scaled_vertical > int_tx_vertical):
    # 抽行
    scale_cr_inserdrawout = "SCALE_CR_DRAWOUT_EN"
    group_line = int(int_tx_vertical / group_num)
    group_drop_line = int((int_scaled_vertical - int_tx_vertical) / group_num)

    p1 = group_line

    p2 = 0
    for i in range(0, p1):
        map_vertical = round((i + 0.5) * int_scaled_vertical / int_tx_vertical - 0.5)
        if (i == (map_vertical - 1)):
            p2 = i
            break

    p3 = int(group_line/group_drop_line)
    p3 = p3 if ((p2 + p3) <= p1) else 0
else:
    scale_cr_inserdrawout = "SCALE_CR_INSERDRAWOUT_DIS"
    p1 = 0
    p2 = 0
    p3 = 0

cx770x_verify_scaled()

print ("#define SCALING_VSCALE", is_vertical_scale)
print ("#define SCALING_HSCALE", is_horizontal_scale)
print ("#define SCALING_NORMAL SCALE_CR_NORMAL_EN")
print ("#define SCALING_DRAW_OUT", scale_cr_inserdrawout)
print ("")
print ("#define SCALING_P1 (%d)" % (p1))
print ("#define SCALING_P2 (%d)" % (p2))
print ("#define SCALING_P3 (%d)" % (p3))
