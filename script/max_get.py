#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import numpy as np

nums_len = 10   # 数组长度
nums_low = 0    # 最小值
nums_high = 20  # 最大值

def sum_get_nums(arr_num, arr_path):
    sum_res = 0
    for i in arr_path:
        sum_res += arr_num[i]

    return sum_res

nums = np.random.randint(nums_low, nums_high, nums_len)
print("生成的随机数组为:\n",nums)

max_current_get = [[0],[0]]

current_get = 0
current_path = [0]

while(current_path[-1] + 1 < (nums.shape[0] - 1)):
    current_path.extend([current_path[-1] + 2])

print(current_path)
current_get = sum_get_nums(nums, current_path)

