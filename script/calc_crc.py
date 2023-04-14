#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

# CRC8 查找表生成
def calc_crc8_table(func_table, func_poly, func_init, func_refin, func_refout, func_xorout):
    for i in range(0, 256):
        temp_crc8 = func_init ^ i;
        for j in range(0, 8):
            if ((temp_crc8 & 0x01) != 0):
                temp_crc8 = (temp_crc8 >> 1) ^ func_poly;
            else:
                temp_crc8 >>= 1;
        func_table[i] = temp_crc8;

buf = [0] * 256;
calc_crc8_table(buf, 0x8C, 0x00, 0, 0, 0);
print(buf);