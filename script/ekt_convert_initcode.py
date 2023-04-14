#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import os
import re

if len (sys.argv) > 1:
    str_input_path = sys.argv[1]
else:
    str_input_path = input ("请输入文件路径：")

if os.path.isfile(str_input_path):
    with open(str_input_path, "r+") as file:
        str_file = file.read()

        str_file = re.sub(r"^#+", "//", str_file, 0)
        str_file = re.sub(r"#", "//", str_file, 0)
        str_file = re.sub(r"mipi.write 0x29 ((0x[0-9a-fA-F][0-9a-fA-F]? +)*0x[0-9a-fA-F][0-9a-fA-F]?)", r"SSD_SEND(0x11, \1);", str_file, 0)
        str_file = re.sub(r"mipi.write 0x05 ((0x[0-9a-fA-F][0-9a-fA-F]? +)*0x[0-9a-fA-F][0-9a-fA-F]?)", r"SSD_SEND(0x10, \1);", str_file, 0)
        str_file = re.sub(r"(0x[0-9a-fA-F][0-9a-fA-F]?)[ ]+(?=0x[0-9a-fA-F][0-9a-fA-F]?)", r"\1, ", str_file, 0)
        print(str_file)
else:
    print ("传入路径未知错误")



