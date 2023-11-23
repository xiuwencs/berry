from collections import Counter
from Apriori import print_2D_list

def simplify(data):
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if data[i][j] not in ['D-', '*-']:
                data[i][j] = 'XX'
    return data

def insert_last(data):
    lst = []
    for i in range(0, len(data)):
        lst.append(data[i])
        if lst[i][-1] != 'D-':
            lst[i].append('D-')
    return lst

def remove_len(lst):
    new_lst = []
    for row in lst:
        if str(row[1]).upper() == 'D-':
            new_lst.append(row[2:])
        else:
            new_lst.append(row[1:])
    # print(new_lst)  # 输出处理后的结果
    return new_lst
def replace_sequence(lst):
    result = []
    count = 0
    local = []
    slot = 0
    i = 0
    while i < len(lst):
        if lst[i] == 'XX' and lst[i+1] == 'D-':
            count += 1
            local.append(i+1)
            if i + 2 == len(lst):
                i += 1
            else:
                i += 2
        elif count < 3:
            local =[]
            i += 1
            count = 0
        elif count >= 3:
            local.pop()
            reversed_list = local[::-1]
            for j in range(0, len(reversed_list)):
                lst.pop(reversed_list[j])
            i = i - count - 1
            count = 0
            slot = reversed_list[-1]-1
        else:
            i += 1
            count = 0
    return lst, slot

def find_most_common_elements(lst):
    count = Counter(lst)
    most_common = count.most_common()
    max_count = most_common[0][1]
    result = [x[0] for x in most_common if x[1] == max_count]
    return int(result[0])

def process(lst):
    slot_lst = []
    updated_lst = []
    new_lst = []
    for i in range(0, len(lst)):
        updated_lst, slot = replace_sequence(lst[i])
        if slot != 0:
            slot_lst.append(slot)
        new_lst.append(updated_lst)
    if slot_lst != []:
        final_slot = find_most_common_elements(slot_lst)
        for i in range(0, len(new_lst)):
            new_lst[i].insert(final_slot, 'D-')
    return new_lst

def post_process(lst):
    front = []
    rear = []
    for i in range(0, len(lst)):
        for j in range(0, len(lst[i])):
            if lst[i][j] == '--':
                for k in range(j - 1, 0, -1):
                    if lst[i][k] == 'D-':
                        front.append(k)
                        break
                for m in range(j + 1, len(lst[i])):
                    if lst[i][m] == 'D-':
                        rear.append(m)
                        break
    print('front:{}'.format(front))
    print('rear:{}'.format(rear))
    if len(set(rear)) >= 2 or len(set(front)) == 1:

        if rear != [] and front != []:
            longest = max(range(len(lst)), key=lambda n: len(lst[n]))
            # solved
            most_rear = find_most_common_elements(rear)
            if len(set(rear)) <= 2:
                lst[longest].insert(max(rear), '--')

        if len(set(front)) == 1:
            lst[0].insert(front[0] + 1, '--')
    # print(lst)
    return lst
def find_first_greater(list, num):
    for x in list:
        if x > num:
            return x

def find_last_occurrence(lst, element):
    if element in lst:
        return len(lst) - lst[::-1].index(element) - 1

def check_merge(lst):
    result = []
    consecutive_count = 1  # 连续出现次数
    for i in range(len(lst) - 1):
        if lst[i:i + 2] == ['XX', 'D-']:
            consecutive_count += 1
        else:
            if consecutive_count >= 3:
                result.extend(['XX'] * consecutive_count)
                result.extend(['D-'])
            else:
                result.extend(lst[i - consecutive_count + 1:i + 1])
            consecutive_count = 1
    if consecutive_count >= 3:
        result.extend(['XX'] * consecutive_count)
        result.extend(['D-'])
    else:
        result.extend(lst[-consecutive_count:])
    return result

def alignment(lst):
    lst = process(lst)
    lst = check_merge(lst)
    for i in range(len(lst)):
        lst[i] = [elem for elem in lst[i] if elem not in ('*-')]
    longest_row = max(lst, key=len)
    lst.remove(longest_row)
    dir = []
    for k in range(0, len(longest_row)):
        if longest_row[k] == 'D-':
            dir.append(k)

    for i in range(len(lst)):
        t = 0
        for j in range(len(lst[i])):
            if t != 0:
                j = j + t
            if j == len(longest_row):
                break
            if lst[i][j] == 'D-' and lst[i][j] != longest_row[j]:
                if 'D-' in lst[i][:j]:
                    l = find_last_occurrence(lst[i][:j], 'D-')
                    inser = l + 1
                else:
                    inser = j - 1
                num = find_first_greater(dir, j)
                if num is not None:
                    t = num - j
                    for k in range(t):
                        lst[i].insert(inser, '--')
    lst.append(longest_row)
    lst = post_process(lst)
    return lst
def process_list(lst):
    unique_rows = []
    last_strings = {}
    for row in lst:
        # 将最后一个字符串之前的部分作为行的唯一标识
        identifier = tuple(row[:-1])
        # 判断是否是第一次遇到该行
        if identifier not in unique_rows:
            unique_rows.append(identifier)
            last_strings[identifier] = int(row[-1])
        else:
            last_strings[identifier] += int(row[-1])  # 最后的字符串相加
    result = []
    for identifier in unique_rows:
        row = list(identifier) + [str(last_strings[identifier])]
        result.append(row)
    return result

def min_and_remove(lst):
    if len(lst) == 0:
        return None
    counter = Counter(lst)
    max_count = max(counter.values())
    most_common_elements = [element for element, count in counter.items() if count == max_count]
    min_element = most_common_elements[0]
    lst.remove(min_element)
    if min_element == 0:
        min_element = min(lst)
        lst.remove(min_element)
    return min_element

def find_most_common_elements(lst):
    count = Counter(lst)
    most_common = count.most_common()
    max_count = most_common[0][1]
    result = [x[0] for x in most_common if x[1] == max_count]
    return int(result[0])

def check_breakpoints(lst):
    l = len(lst)
    n = 0
    record = []
    for i in range(0, l):
        for j in range(0, len(lst[i])):
            if lst[i][j] == 'D-':
                record.append(j)
    most_comm = find_most_common_elements(record)
    count = record.count(most_comm)
    counter = Counter(record)
    max_count = max(counter.values())
    max_elements = [element for element, count in counter.items() if count == max_count]
    most_comm = max(max_elements)
    for m in range(0, l):
        if '--' in lst[m][:most_comm]:
            n += 1
            break_index = lst[m].index('--')
            if 'XX' not in lst[m][break_index:]:
                lst[m][break_index] = 'D-'
                n = 0
    if count == l and n > 0 :
        for k in range(0, l):
            lst[k].insert(most_comm, '--')
            lst[k] = remove_dashes(lst[k], most_comm)
    return lst
def remove_dashes(lst, n):
    lst_a = []
    index = n + 1  # 设定起始位置
    for i in range(index, len(lst)):
        if lst[i] != '--':
            lst_a.append(lst[i])
            new_lst = lst[:index] + lst_a
    return new_lst

def mark_and_remove(lst):
    lst = check_breakpoints(lst)
    results = []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == '--':
                results.append(j)
    if results == []:
        print('The protocol does not have variable length fields!')
        return 0
    for i in range(len(lst)):
        if max(results)+2 < len(lst[i]) and lst[i][max(results)+2] == 'D-':
            lst[i].insert(max(results) + 2, '/')
        else:
            lst[i].insert(max(results) + 1, '/')
        lst[i].insert(min(results), '/')
        lst[i] = [elem for elem in lst[i] if elem not in ('--', 'D-', '*-')]

    for i in range(0, len(lst)):
        if lst[i][-1] == '/':
            for j in range(0, len(lst[i])):
                if lst[i][j] not in ('XX', '/'):
                    cup = lst[i][j]
                    lst[i][j] = '/'
                    lst[i][-1] = cup

    new_lst = process_list(lst)
    for i in range(0, len(new_lst)):
        for j in range(0, len(new_lst[i]) - 1):
            if new_lst[i][0] == '/':
                new_lst[i][0], new_lst[i][1] = new_lst[i][1], new_lst[i][0]
            if new_lst[i][j] == '/' and new_lst[i][j - 1] == '/':
                new_lst[i][j], new_lst[i][j + 1] = new_lst[i][j + 1], new_lst[i][j]
    print('The final result:')
    print_2D_list(sorted(new_lst, key=len))
    vl = []
    for i in range(0, len(new_lst)):
        for j in range(0, len(new_lst[i])):
            if new_lst[i][j] == '/':
                vl.append(j)
    vl_new = list(set(vl))
    min_vl = min_and_remove(vl)
    result = []
    for i in range(0, len(vl_new)):
        length = vl_new[i] - min_vl - 1
        if length > 0:
            result.append(length)
    print('offset:{}'.format(min_vl))
    print('length:{}'.format(result))
    return lst
