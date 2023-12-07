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
from IntegrateAlignment import result_output
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

def print_final(four_dimensional_list, output_file_path):
    if four_dimensional_list == 0:
        print('输出为转换文件')
        return 0
    # 打开文件并写入数据
    with open(output_file_path, 'w') as file:
        for three_dimensional_list in four_dimensional_list:
            for two_dimensional_list in three_dimensional_list:
                for one_dimensional_list in two_dimensional_list:
                    # 将每个元素连接为字符串，使用制表符分隔，然后写入文件
                    file.write('\t'.join(one_dimensional_list) + '\n')

def threeDim_trans_2(three_dimensional_list):
    two_dimensional_list = [row for matrix in three_dimensional_list for row in matrix]
    return two_dimensional_list


if __name__ == '__main__':
    pcapng_file = input('请输入文件路径：')
    trans_file = input('请输入转换文件txt路径：')
    output_file = input('请输入输出文件名：')

    # 导入文件
    import_data = import_file(pcapng_file, trans_file)

    # 消息类型聚类
    cluster_data = cluster(import_data)

    # 切割头部和负载
    cluster_data, lst = header_dividing(cluster_data)
    com = find_most_frequent(lst)
    cluster_data = check_long(cluster_data, com)

    # 在每个聚类中进行关联分析和数据整合
    sequences = []
    print_result = []
    remain = []
    for i in range(len(cluster_data)):
        trans = []
        result = []
        re = []
        unique_matrix = []
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
    remain = threeDim_trans_2(remain)
    lst = mark_and_remove(align_result)
    print('remain:{}'.format(len(remain)))
    print_result = threeDim_trans_2(print_result)
    print('data:{}'.format(len(print_result)))
    print('total:{}'.format(len(remain) + len(print_result)))

    # 输出
    final_result = result_output(cluster_data, lst)
    print_final(final_result, output_file)

