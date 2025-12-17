def remove_consecutive_numbers(lst):
    # 创建一个新列表，用于存储结果
    result = []
    # 初始化当前连续数序列的起始数为列表第一个数
    current_sequence_start = lst[0]

    # 遍历列表，从第二个数开始
    for i in range(1, len(lst)):
        # 如果当前数是上一个数的下一个数，则继续当前连续数序列
        if lst[i] == lst[i - 1] + 1:
            continue
        # 否则，当前数打破了连续数序列，将前一个连续数序列的最大数加入结果列表中
        result.append(lst[i - 1])
        # 更新当前连续数序列的起始数为当前数
        current_sequence_start = lst[i]

    # 最后一个连续数序列的最大数加入结果列表中
    result.append(lst[-1])

    return result

def fix_field(matrix):
    # 获取最短行的长度，避免索引超出范围
    min_length = min(len(row) for row in matrix)
    # 存储元素全部相同的列的索引
    uniform_columns = []

    # 遍历每一列，范围在最短行的长度内
    for col in range(0, min_length):
        # 获取当前列的第一个元素
        first_element = matrix[0][col]
        # 检查当前列的每一个元素是否都等于第一个元素，并且列索引不超出每行的长度
        # if all(len(row) > col and row[col] == first_element for row in matrix) and first_element != '00':
        if all(len(row) > col and row[col] == first_element for row in matrix):
            # 如果当前列元素全部相同，则记录该列的索引
            uniform_columns.append(col)
            # uniform_columns.append(col + 1)
    if uniform_columns:
        print(uniform_columns)
        result = remove_consecutive_numbers(uniform_columns)
        return result

    return uniform_columns

def fixed(file_name):
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

    # 删除所有子列表中的'/'
    matrix_without_slash = [[elem for elem in sublist if elem != '/'] for sublist in import_data]

    # 序列对比
    fix_offset = fix_field(matrix_without_slash)
    if fix_offset:
        print('fixed offset:{}'.format(fix_offset))
    else:
        print('No fixed fields exist')
