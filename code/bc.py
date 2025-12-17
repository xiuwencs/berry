import numpy as np
from collections import defaultdict
from Matching import matching
import time
# from IntegrateAlignment import print_all
def count_matching_bits(hex1, hex2):
    # 将十六进制数转换为二进制字符串
    bin1 = bin(int(hex1, 16))[2:].zfill(len(hex1) * 4)
    bin2 = bin(int(hex2, 16))[2:].zfill(len(hex2) * 4)

    # 初始化相同位数的计数器
    matching_count = 0

    # 对比两个二进制字符串，计算相同位数的数量
    for bit1, bit2 in zip(bin1, bin2):
        if bit1 == bit2:
            matching_count += 1
    result = matching_count/8

    return result

def count_matching_unbits(hex1, hex2):
    # 将十六进制数转换为二进制字符串
    bin1 = bin(int(hex1, 16))[2:].zfill(len(hex1) * 4)
    bin2 = bin(int(hex2, 16))[2:].zfill(len(hex2) * 4)

    # 初始化相同位数的计数器
    matching_count = 0

    # 对比两个二进制字符串，计算相同位数的数量
    for bit1, bit2 in zip(bin1, bin2):
        if bit1 != bit2:
            matching_count += 1
    result = matching_count/8

    return result


def consistency_calculation(hex_list):
    bc = []
    unbc = []
    for i in range(0, len(hex_list)):
        if hex_list[i] == '/':  # 如果当前位置是'/'，跳过
            continue

        # 寻找下一个不是'/'的位置
        j = i + 1
        while j < len(hex_list) and hex_list[j] == '/':
            j += 1

        if j >= len(hex_list):  # 如果没有找到下一个有效值，结束循环
            break

        matching_count = count_matching_bits(hex_list[i], hex_list[j])
        bc.append(matching_count)
        matching_count = count_matching_unbits(hex_list[i], hex_list[j])
        unbc.append(matching_count)
    return bc, unbc

def bc(file_name):
    # 二维列表
    import_data = []
    # 读取文本文件
    with open(file_name, "r") as file:
        # 逐行读取内容
        for line in file:
            # 移除每行末尾的换行符
            line = line.strip()
            # 分割每行内容，以制表符分隔
            values = line.split('\t')
            # 将每行的字符串列表添加到二维列表中
            import_data.append(values)

    # 归零
    for i in range(0, len(import_data)):
        slash_indices = [j for j, x in enumerate(import_data[i]) if x == '/']
        if len(slash_indices) == 2:
            start_index = slash_indices[0]
            end_index = slash_indices[1]
            import_data[i][start_index + 1: end_index] = ['00'] * (end_index - start_index - 1)

    data = []
    for i in range(0, len(import_data)):
        hex_list = import_data[i]
        result, unresult = consistency_calculation(hex_list)
        data.append(result)
    # 特征点
    consistent_x_values, significant_x_values, scattered_x_values = matching(data)
    print("type 1:", significant_x_values)
    print("type 2:", scattered_x_values)
