#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import os
import csv
import openpyxl

if len (sys.argv) > 1:
    str_file_path = sys.argv[1]
else:
    str_file_path = input ("请输入文件路径：")

if os.path.isfile(str_file_path):
    str_file_dir = os.path.dirname(str_file_path)
    str_file_base = os.path.basename(str_file_path)
    str_file_base = os.path.splitext(str_file_base)[0]
    if str_file_dir == "":
        str_fileout_path = os.path.join(".", str_file_base + ".xlsx") # 兼容linux和windows路径
    else:
        str_fileout_path = os.path.join(str_file_dir, str_file_base + ".xlsx")

    with open (str_file_path, "r") as file_sheet:
        csv_sheet_reader = csv.reader(file_sheet, delimiter=',')

        # 将csv文件经过预处理去掉第一行和第一列并转换成列表
        list_csv_data = []
        for index, item in enumerate(csv_sheet_reader):
            if (index == 0):
                continue
            list_csv_data.append(item[2])

        # 删掉无意义的符号
        list_data = []
        for item in list_csv_data:

            if ((item == "Start bit") or (item == "Stop bit")):
                continue

            list_data.append(item)

        # 将一维列表转换成二维列表
        list_sheet = [[]]
        for item in list_data:
            if (item == "[00]"):
                list_sheet.append([])
            else:
                if (len(list_sheet[-1])==0):
                    list_sheet[-1].extend(item)
                else:
                    list_sheet[-1][0] += item
    #生成xlsx文件
    workbook = openpyxl.Workbook()
    sheet = workbook.active #Excel页签标识

    for list_data_row in list_sheet:
        sheet.append(list_data_row)

    #保存为xlsx文件，名字可以随意写
    workbook.save(str_fileout_path)

else:
    print ("无法识别路径")