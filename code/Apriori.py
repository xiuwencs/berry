import pandas as pd
import numpy as np
import itertools as it
import time
import sys
import os
from itertools import chain
from collections import Counter
from collections import OrderedDict
import csv

# 去除集合矩阵（i，j）None值，便于计数以及算法，常规的pandas是用来数据清洗和数据填充的，没办法解决这种问题
def Non_deal(df):
    list_data = []
    rows = len(df)
    for i in range(0, rows):
        list = df[i]
        list_con = []
        cols = len(list)
        for j in range(0, cols):
            if list[j] != "nan":
                list_con.append(list[j])  # 如果用remove法需要倒序去除，否则无法去除干净（因为每一次去除会导致len-1)
        list_data.append(list_con)
    return list_data

def modify_list(lst):
    for inner_lst in lst:
        consecutive_d_count = 0
        modified_lst = []
        for element in inner_lst:
            if element == 'D-':
                if consecutive_d_count == 0:
                    modified_lst.append(element)
                consecutive_d_count += 1
            else:
                modified_lst.append(element)
                consecutive_d_count = 0
        inner_lst[:] = modified_lst
    return lst

def remove_duplicate(rows):
    unique_rows = []
    for row in rows:
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows

# 目的是得到备选1-项集
def element_list(df):
    list_in = Non_deal(df)
    list_m = []
    for i in range(0, len(list_in)):
        for j in range(0, len(list_in[i])):
            list_m.append(list_in[i][j])
    ordered_dict = OrderedDict.fromkeys(list_m)
    new_list = list(ordered_dict.keys())
    rows, cols = len(new_list), 1
    new_list = [[new_list[i * cols + j] for j in range(cols)] for i in range(rows)]
    return new_list

# 目的是进行k-1-频繁项集合的重组为k项目集合
def creat_connect(list_c, n):  ##实现集合内的重组，例如2-项集合重组为3-项集
    new_list = []
    # print(list_c)             #!!!
    for i in range(0, len(list_c)):
        list_a = []
        for j in range(i + 1, len(list_c)):
            list_b = list_c[i]
            list_d = []
            for k in range(0, n):
                list_d.append(list_c[j][k])
            list_a = list_b + list_d
            list_a = remove_duplicate(list_a)
            new_list.append(str(list_a))
        new_list = remove_duplicate(new_list)
    New_list = []
    for i in range(0, len(new_list)):
        new_list[i] = eval(new_list[i])
        if len(new_list[i]) == n + 1:
            New_list.append(new_list[i])
    return New_list

# 输出每个k-项频繁集的候选集的比率
def sup_rate(df, data):
    m = len(data)  # 事务总数
    item_set_list = []
    for i in range(0, len(df)):
        n = 0
        list_n = []
        for j in range(0, len(data)):
            if (set(df[i]) <= set(data[j])) == True:
                n += 1
        list_n.append(df[i])
        list_n.append(round(n / m, 2))
        item_set_list.append(list_n)
    return item_set_list

# 输出每个1-项频繁集的候选集的个数，上有比率写法，两者无本质区别，都可以使用
def sup_count_1(df, data):  # 输出每个1-项频繁集的候选集的次数
    item_set_list = []
    for i in range(0, len(df)):
        n = 0
        list_n = []
        for j in range(0, len(data)):
            if df[i][0] in data[j]:
                n += 1
        list_n.append(df[i])
        list_n.append(n)
        for j in range(0, len(data)):
            if df[i][0] in data[j]:
                for k in range(0, len(data[j])):
                    if (data[j][k] == df[i][0]) == True:
                        list_n.append(k)
        item_set_list.append(list_n)
        # print(list_n)
    return item_set_list

# 输出每个k-项频繁集的候选集的个数，上有比率写法，两者无本质区别，都可以使用
def sup_counts(df, data):  # 输出每个1-项频繁集的候选集的次数
    item_set_list = []
    for i in range(0, len(df)):
        n = 0
        list_n = []
        for j in range(0, len(data)):
            if (set(df[i]) <= set(data[j])) == True:
                n += 1
        list_n.append(df[i])
        list_n.append(n)
        item_set_list.append(list_n)
    return item_set_list

# the location for
def sup_satisfy_item_location(data):
    Good_list1 = element_list(data)
    dt = sup_count_1(Good_list1, data)
    item_location_list = []
    for i in range(0, len(dt)):
        item_location_list.append(dt[i])
    return item_location_list

def item_1_candidates_fre(data):
    Good_list1 = element_list(data)
    dt = sup_counts(Good_list1, data)
    return dt

# 得到满足最小支持度阈值的关联规则（find——rule of min-sup-rate item）
def sup_satisfy_item(data, min_suprate):
    n = len(data)  # 事务总数
    dt = item_1_candidates_fre(data)
    m = len(dt)
    All_freitem_list = []
    k_list = []
    for k in range(0, m):
        k_apriori = []
        for j in range(0, len(dt)):
            if dt[j][-1] >= min_suprate * n:  ##减枝过程
                k_apriori.append(dt[j][0])
        dt = sup_counts(creat_connect(k_apriori, k), data)
        if len(k_apriori) != 0:
            All_freitem_list.append(k_apriori)
        else:
            break
    return All_freitem_list


def Ksubset_get(df):  # 获得非空子集（前提条件是频繁项集，否则数量太多，很难挖掘）
    n = len(df)
    k = len(df[0])
    All_nzsubset = []
    for num in range(n):
        for i in it.combinations(df, num + 1):  # 调用it.combination 函数
            All_nzsubset.append(list(i))
    return All_nzsubset

def Find_rule_apriori(data, Sup_satisfy_item, min_suprate, min_confi):
    a = len(data)  # 事务总数
    l = len(Sup_satisfy_item)  # 获得频繁项集集合的集合长度（多少种长度的频繁项）
    new_list = []
    all_frequent = []
    for i in range(0, l):  # 无需对频繁1项集合找寻关联规则，直接从频繁二项集的集合进行扫寻循环
        Sup_satisfy_itemi = Sup_satisfy_item[i]  # 得到一个频繁i+1项集合的列表的列表
        m = len(Sup_satisfy_itemi)
        for j in range(0, m):  # 为对每一个频繁项进行扫寻，因此需要再做一次for循环
            Prule = Sup_satisfy_itemi[j]
            list1 = []
            list1.append(Prule)
            item_counts1 = sup_counts(list1, data)[0][-1]  # 首先需要得到这一个频繁项集的支持度计数，或者计算频数也可以
            list1.clear()
            prerule_find = Ksubset_get(Prule)  # 得到这一个频繁项集集合的所有非空集合，方便进行关联规则的重组
            prerule_find.remove(prerule_find[-1])  # 删除全集
            q = len(prerule_find)  # 得到排除全集后的关联重组列表的长度，以便进行for循环
            all_frequent = []
            for z in range(0, q):
                list2 = []
                list2.append(prerule_find[z])
                item_counts2 = sup_counts(list2, data)[0][-1]  # 得到每一个关联重组后项集的支持度（或频数）
                list2.clear()
                if item_counts2 > 0:
                    Confi_item = item_counts1 / item_counts2  # 得到置信度

                    if Confi_item >= min_confi:  # 置信度减除
                        n = len(prerule_find[z])
                        list3 = Prule[:]
                        for d in range(0, len(list3)):
                            all_frequent.append(list3[d])

                        for o in range(0, n):
                            # print("rules:")
                            list3.remove(str(prerule_find[z][o]))
    all_frequent = list(set(all_frequent))
    return all_frequent

def Find_final_location(Sup_satisfy_item_location):
    for i in range(0, len(Sup_satisfy_item_location)):
        Sup_satisfy_item_location[i][0] = (Sup_satisfy_item_location[i][0][0])
    for j in range(0, len(Sup_satisfy_item_location)):
        count = Counter(Sup_satisfy_item_location[j][2:])
        most_common = count.most_common()
        max_count = most_common[0][1]
        result = [x[0] for x in most_common if x[1] == max_count]
        Sup_satisfy_item_location[j] = Sup_satisfy_item_location[j][:2]
        Sup_satisfy_item_location[j].append(result)
    return Sup_satisfy_item_location

def fre_trans(lst):
    trans_list = []
    for i in range(0, len(lst)):
        for j in range(0, len(lst[i][-1])):
            result = []
            result.append(lst[i][:2])
            result.append(lst[i][-1][j])
            trans_list.append(result)
    final_list = [[item[0][0], item[0][1]] + ([item[1]] if len(item) > 1 else []) for item in trans_list]
    # print('final_list:\n{}'.format(final_list))
    return final_list

def remove_duplicate(lst):
    temp_set = set()  # 存储每行第一个元素的集合
    new_lst = []  # 用于存储每行第一个元素不重复的行
    dup_lst = []  # 用于存储每行第一个元素重复的行
    for row in lst:
        key = row[0]
        if key not in temp_set:
            temp_set.add(key)
            new_lst.append(row)
        else:
            new_lst = [r for r in new_lst if r[0] != key]
    return new_lst

def Find_location_with_fre(Sup_satisfy_item_location, all_frequent, sup, data):
    lst = []
    Sup_location = Find_final_location(Sup_satisfy_item_location)
    print(all_frequent)
    for i in range(0, len(all_frequent)):
        for j in range(0, len(Sup_location)):
            if (all_frequent[i] == Sup_satisfy_item_location[j][0] and all_frequent[i] != '00') == True:
                lst.append(Sup_location[j])
    print('lst:\n{}'.format(lst))
    final_list = remove_duplicate(fre_trans(lst))
    final_list = fre_trans(lst)
    print('final_list:\n{}'.format(final_list))
    list_q = []
    list_q.append(100)
    pre_list = []
    record_list = []
    behind_list = []
    for i in range(0, len(final_list)):
        for j in range(0, len(final_list)):
            if final_list[i][-1] == final_list[j][-1] + 1 or final_list[j] == '00':          # notice!!!need to modify
                pre_list.append(final_list[j])
    a = 0
    for i in range(0, len(final_list)):
        for j in range(0, len(pre_list)):
            if final_list[i][-1] == pre_list[j][-1]:
                a = 0
                break
            else:
                a = 1
        if a == 1:
            behind_list.append(final_list[i])
    if pre_list != []:
        all_list = behind_list + pre_list   #important!
    else:
        all_list = final_list
        behind_list = final_list

    for j in range(0, len(all_list)):
        for d in range(0, len(data)):   # row by row
            t = all_list[j][-1]
            m = 0
            for q in range(0, len(list_q)):
                if list_q[q] < t:
                    m += 1
            t = t+m+1
            if j < len(behind_list):
                data[d].insert(t, 'D-')
            elif j >= len(behind_list) and all_list[j][0] == '00':
                data[d].insert(t, '*-')
            elif j >= len(behind_list):
                data[d].insert(t, 'D-')
        list_q.append(all_list[j][-1])

    modified_data = modify_list(data)
    print(modified_data[0])
    return modified_data

def print_2D_list(data):
    for i in range(len(data)):
        print(data[i])
    print('\n')

def apriori_find(data):
    minsup,minconfi=(0.5, 1)
    start = time.time()
    print(data[0])
    Sup_satisfy_item = sup_satisfy_item(data, minsup)  # 获得满足支持度的频繁项集，第一项为频繁1项集合的集合，以此类推。

    all_frequent = Find_rule_apriori(data, Sup_satisfy_item, minsup, minconfi)
    if all_frequent != []:
        lst = Find_location_with_fre(sup_satisfy_item_location(data), all_frequent, minsup, data)
        return lst
    if Sup_satisfy_item != []:
        print('no frequent apriori!')
        print('no-apriori-frequent:{}'.format(Sup_satisfy_item[0]))
        original_list = Sup_satisfy_item[0]
        new_list = [item[0] for item in original_list]
        lst = Find_location_with_fre(sup_satisfy_item_location(data), new_list, minsup, data)
        return lst
    else:
        print('no result!')
    end = time.time()
    print('Running time: {0} Seconds'.format(end - start))