#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import os
import csv

if len (sys.argv) > 1:
    str_file_path = sys.argv[1]
else:
    str_file_path = input ("请输入文件路径:")

if os.path.isfile(str_file_path):
    str_file_dir = os.path.dirname(str_file_path)
elif os.path.isdir(str_file_path):
    print ("传入参数的路径无效")
    exit(-1)
else:
    print ("传入参数未知错误")
    exit(-1)

## 打开csv文件
with open (str_file_path, "r") as file_sheet:
    csv_sheet_reader = csv.reader(file_sheet, delimiter=',')
    list_sheet_reader = [item[2] for item in csv_sheet_reader][1:]  # 提取第二列数据

## 分析dslogic的csv文件并将每包数据转换为list
list_package = []
for item in list_sheet_reader:
    if ((item == "ACK") or (item == "NACK") or (item == "Stop")):
        continue

    if (item == "Start repeat"):
        item = "Start"

    if (item.find(':') != -1):
        item = item.split(":")[1]; # 以':'为界定符分割文本
        item = item.strip(" "); # 去除字符串中的空格，即':'后面可能存在的空格

    if (item == "Start"):
        list_package.append([])
    else:
        list_package[-1].append(item)

## 分析i2c读写关系并转换为字典
dict_package={}
last_write_postion = -1
for index, item in enumerate(list_package):
    if (not item):
        continue

    if (item[0] == "Write"):
        last_write_postion = index
    elif (item[0] == "Read"):
        if (index == 0):
            temp_key = 'initial'
        else:
            temp_key = ''.join(list_package[last_write_postion][2:])
        temp_value = ''.join(item[2:])

        if (temp_key in dict_package):
            if (last_write_postion == index-1):
                dict_package[temp_key].append(temp_value)
            else:
                dict_package[temp_key][-1].join(temp_value)
        else:
            dict_package[temp_key] = [temp_value]

## 分析回复固定值和动态值的
dict_res = {}
dict_func = {}
dict_func_norepet = {}

for key in dict_package:
    is_res = all(dict_package[key][0] == item for item in dict_package[key])    # 判断回复值是否相同

    if (is_res):
        dict_res[key] = dict_package[key][0]
    else:
        dict_func[key] = dict_package[key]
        dict_func_norepet[key] = list(set(dict_package[key]))

## 生成代码
def strhex_to_strarray(func_str):
    # 将hex的字符串转换成C语言0x格式
    PARAM_SPLIT = 2
    PARAM_MAX_PER = 16
    list_str_hex = ["0x" + func_str[i:i+PARAM_SPLIT] for i in range(0,len(func_str),PARAM_SPLIT)]
    # 如果数组数量超过每行最大数量PARAM_MAX_PER,则分行
    list_str_hex = [list_str_hex[i:i+PARAM_MAX_PER] for i in range(0,len(list_str_hex),PARAM_MAX_PER)]

    if len(list_str_hex) <= 1:
        # 单行数组表示
        return " {" + ", ".join(list_str_hex[0]) + "};\n"
    else:
        # 多行数组表示
        return "\n{\n    " + ",\n    ".join(", ".join(item) for item in list_str_hex) + "\n};\n"

# 常量生成
str_match_key = "//// Command\n"
str_match_res_key = "//// Respone\n"
str_key_res_table = """#define MATCH_I2C_KEYTOFUNC(key) {0x00, sizeof(match_key##key), 0x0000, match_key##key, match_func_key##key}
#define MATCH_I2C_KEYTORES(key) {0x01, sizeof(match_key##key), sizeof(match_res_key##key), match_key##key,  match_res_key##key}
const I2CKeyResTable_TypeDef i2ckeyrestable[] =\n{\n"""

for key in dict_func:
    str_match_key += "const uint8_t match_key" + key + "[] =" + strhex_to_strarray(key)
    for index, item in enumerate(dict_func_norepet[key]):
        str_match_res_key += "const uint8_t match_res_key" + key + "_" + str(index) + "[] =" + strhex_to_strarray(item)
    str_key_res_table += "    MATCH_I2C_KEYTOFUNC(" + key + "),\n"
str_key_res_table += "\n"
for key in dict_res:
    str_match_key += "const uint8_t match_key" + key + "[] =" + strhex_to_strarray(key)
    str_match_res_key += "const uint8_t match_res_key" + key + "[] =" + strhex_to_strarray(dict_res[key])
    str_key_res_table += "    MATCH_I2C_KEYTORES(" + key + "),\n"
str_key_res_table = str_key_res_table[:-2] + "\n};\n#undef MATCH_I2C_KEYTOFUNC\n#undef MATCH_I2C_KEYTORES\n"

# 函数生成
str_match_func_key_declare = "//// Function\n"
str_match_func_key_realize = ""
str_match_var_key = ""

for key in dict_func:
    str_match_func_key_declare += "void match_func_key" + key + "(void);\n"
    str_match_var_key += "uint8_t match_var_key" + key + " = 0;\n"

    str_match_func_key_realize += "void match_func_key" + key + "(void)\n{\n    switch(match_var_key" + key + ")\n    {\n"
    for index, item in enumerate(dict_func_norepet[key]):
        # 合并重复的case项
        for index_2, item_2 in enumerate(dict_func[key]):
            if (item_2 == item):
                str_match_func_key_realize += "        case " + str(index_2) + ":\n"
        str_match_func_key_realize += "        match_i2c_response(match_res_key" + key + "_" + str(index) + ");\n        match_var_key" + key + "++;\n        break;\n\n"
    str_match_func_key_realize += "        default:\n        match_i2c_response(match_res_key" + key + "_0);\n        match_var_key" + key + " = 0;\n        break;\n    }\n}\n\n"

if (dict_func):
    print (str_match_key + "\n" + str_match_res_key + "\n" + str_match_func_key_declare + "\n" + str_key_res_table + "\n" + str_match_var_key + "\n" + str_match_func_key_realize)
else:
    print (str_match_key + "\n" + str_match_res_key + "\n" + str_key_res_table)