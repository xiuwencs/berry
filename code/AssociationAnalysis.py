# -*- coding: utf-8 -*-
from Apriori import apriori_find
from Apriori import print_2D_list

def len_sort(data):
    result = {}
    for sublist in data:
        length = len(sublist)
        if length not in result:
            result[length] = [sublist]
        else:
            result[length].append(sublist)
    sort_list = []
    for key in result:
        sort_list.append(result[key])
    print('len_sort successfully!total:{}'.format(len(sort_list)))
    return sort_list

def segment(data):
    n = 0
    final = []
    remain = []
    for i in range(len(data)):
        lst = []
        if len(data[i]) > 5:
            print('list{}:'.format(i + 1))
            lst = apriori_find(data[i])
            final.append(lst)
        else:
            print('This len of data do not have enough lists!')
            n += 1
            remain.append(data[i])
    print('drop{}:'.format(n))
    return final, remain

def print_num(data):
    each = []
    for i in range(0, len(data)):
        each.append(len(data[i]))
    print(each)


def insert_len(data):
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            data[i][j].insert(0, str(len(data[i][j])))
    print("insert_len successfully!")
    return data


def iteration(data):
    result = [item for sublist in data for item in sublist]
    data = len_sort(result)
    return data

def print_first_and_num(data):
    print('\n')
    lst = []
    for i in range(0, len(data)):
        lst.append(data[i][0])
    print('Number of pieces corresponding to each length:')
    each = []
    for i in range(0, len(data)):
        each.append(len(data[i]))
        print(lst[i])
    print(each)
    return lst

