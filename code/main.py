# -*- coding: utf-8 -*-
from Import_hex import import_file
from Apriori import print_2D_list
from IntegrateAlignment import alignment
from IntegrateAlignment import mark_and_remove
from Classification import cluster
from AssociationAnalysis import segment
from IntegrateAlignment import remove_len
from IntegrateAlignment import simplify
from IntegrateAlignment import insert_last
from collections import defaultdict
from Classification import header_dividing
from Classification import check_long
from Classification import find_most_frequent

def remove_duplicate(rows):
    unique_rows = []
    duplicate_count = defaultdict(int)
    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in unique_rows:
            unique_rows.append(row_tuple)
        duplicate_count[row_tuple] += 1
    unique_rows = [list(row) for row in unique_rows]

    for row in unique_rows:
        row.append(str(duplicate_count[tuple(row)]))
    return unique_rows

def threeDim_trans_2(three_dimensional_list):
    two_dimensional_list = [row for matrix in three_dimensional_list for row in matrix]
    return two_dimensional_list

if __name__ == '__main__':
    pcapng_file = input('请输入文件路径：')
    trans_file = input('请输入转换文件txt路径：')

    # 导入文件
    import_data = import_file(pcapng_file, trans_file)

    # 消息类型聚类
    cluster_data = cluster(import_data)

    # 切割头部和负载
    cluster_data, lst = header_dividing(cluster_data)
    com = find_most_frequent(lst)
    cluster_data = check_long(cluster_data, com)

    # 在每个聚类中进行关联分析和数据整合
    final_lst = []
    sequences = []
    print_result = []
    remain = []
    num = []
    for i in range(len(cluster_data)):
        trans = []
        result = []
        re = []
        unique_matrix = []
        unique_rows = []
        # 关联分析
        data, re = segment(cluster_data[i])
        print("segment successfully!")
        trans = threeDim_trans_2(data)

        # 数据整合
        result = remove_len(trans)
        print_result.append(insert_last(result))
        simp = simplify(insert_last(result))
        unique_matrix = remove_duplicate(simp)
        sequences.append(unique_matrix)
        remain.append(re)

    # 对齐
    sequences = threeDim_trans_2(sequences)

    print('alignment:')
    align_result = alignment(sequences)
    print_2D_list(sorted(align_result, key=len))

    # 标记字段位置和长度
    lst = mark_and_remove(align_result)
    remain = threeDim_trans_2(threeDim_trans_2(remain))
    print('remain:{}'.format(len(remain)))
    print_result = threeDim_trans_2(print_result)
    print('data:{}'.format(len(print_result)))
    print('total:{}'.format(len(remain) + len(print_result)))
