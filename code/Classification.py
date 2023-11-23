from Import_hex import import_file
from collections import Counter
import math
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

def cluster(data):
    max_length = max(len(sublist) for sublist in data)
    data_padded = [sublist + ['00'] * (max_length - len(sublist)) for sublist in data]
    data_int = [[int(val, 16) for val in sublist] for sublist in data_padded]

    # 自动确定聚类数
    max_clusters = 5
    best_score = -1
    best_clusters = 2
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(data_int)
        labels = kmeans.labels_
        score = silhouette_score(data_int, labels)
        if score > best_score:
            best_score = score
            best_clusters = k
    print('最佳聚类数：{}'.format(best_clusters))

    kmeans = KMeans(n_clusters=best_clusters, random_state=0).fit(data_int)
    labels = kmeans.labels_
    result = [[] for _ in range(max(labels) + 1)]
    for i, sublist in enumerate(data):
        result[labels[i]].append(sublist)

    return result

def remove_duplicate(rows):
    unique_rows = []
    duplicate_count = defaultdict(int)

    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in unique_rows:
            unique_rows.append(row_tuple)
        duplicate_count[row_tuple] += 1

    unique_rows = [list(row) for row in unique_rows]
    return unique_rows
def calculate_shannon_entropy(data):
    num_rows = len(data)
    num_cols = len(data[0])
    shannon_entropies = []
    for col in range(num_cols):
        column_values = [data[row][col] for row in range(num_rows)]
        value_counts = Counter(column_values)
        prob_dist = [count / num_rows for count in value_counts.values()]
        shannon_entropy = -sum(prob * math.log2(prob) for prob in prob_dist)
        shannon_entropies.append(shannon_entropy)
    return shannon_entropies

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

def euclidean_distance(vec1, vec2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(vec1, vec2)))

def find_most_frequent(lst):
    counter = Counter(lst)
    most_common = counter.most_common(1)
    return most_common[0][0]

def cut_pay(sudden, data):
    for i in range(0, len(data)):
        data[i] = data[i][:sudden]
    return data
def boundary(original_list):
    differences = [y - x for x, y in zip(original_list[:-1], original_list[1:])]
    max_r = max(differences)
    index_max = differences.index(max_r)
    min_d = min(differences)
    index_min = differences.index(min_d)
    print('max:{}, index:{}'.format(max_r, index_max))
    print('min:{}, index:{}'.format(min_d, index_min))
    add = max_r + min_d

    part_max = max(differences[:20])
    part_max_index = differences[:20].index(part_max)
    part_min = min(differences[:20])
    part_min_index = differences[:20].index(part_min)

    if len(set(differences)) > 3:
        differences.remove(max_r)
        differences.remove(min_d)
        max_r2 = max(differences)
        index_max2 = differences.index(max_r2)
        min_d2 = min(differences)
        index_min2 = differences.index(min_d2)
        print('max_2:{}, index_2:{}'.format(max_r2, index_max2))
        print('min_2:{}, index_2:{}'.format(min_d2, index_min2))

    if max_r > 0 and add > 0.5:
        print('There is no sudden drop point')
        sudden = index_max + 1
        if abs(min_d) * 3 < max_r:
            sudden = len(original_list)
        elif abs(abs(min_d + min_d2) - max_r) < 0.2:
            sudden = max(index_max, index_max2) + 1
    elif len(set(differences)) < 3:
        sudden = len(original_list)
    elif -0.5 < add < 0.5:
        print('There is a sudden drop point')
        if max_r2 + min_d2 < 0.5 and index_min2 < index_min and index_max2 < index_max and index_max2 < index_min2 and abs(min_d - min_d2) < 1.1 and abs(max_r - max_r2) < 1.1 and index_min - index_min2 < 10 :
            sudden = index_min2 + 1
        elif max_r2 + min_d2 < 0.5 and index_max2 > index_min2 and abs(max_r - max_r2) < 1 and abs(min_d - min_d2) < 1 and abs(index_max2 - index_max) > 1 and index_min - index_min2 < 10:#snmp
            sudden = index_min2 + 2
        elif index_min > 0.3 * len(original_list):
            if index_max - index_max2 > 1:
                sudden = index_max2 + 2
            elif max_r - max_r2 < 0.25:
                sudden = index_min2 + 3
            else:
                sudden = index_max + 1
        else:
            sudden = max(index_max, index_max2) + 1
            if sudden > 15:
                sudden = 15
    else:
        sudden = index_max + 1
    if sudden > 15:
        if part_max_index > 2:
            sudden = part_max_index + 1
        elif part_min_index > 2:
            sudden = part_min_index + 1
        else:
            sudden = index_max + 1
    if sudden < 2:
        sudden += 12
    print('sudden:{}'.format(sudden))
    return sudden

def header_dividing(cluster_data):
    entropy = []
    rise = []
    drop = []
    lst = []
    for i in range(0, len(cluster_data)):
        cluster_data[i] = len_sort(cluster_data[i])
        for j in range(0, len(cluster_data[i])):
            if len(cluster_data[i][j]) > 5:
                entropies = calculate_shannon_entropy(cluster_data[i][j])
                entropy.append(entropies)
                print('entropies:{}'.format(entropies))
                sudden = boundary(entropies)
                for k in range(0, len(cluster_data[i][j])):
                    lst.append(sudden)
                cluster_data[i][j] = cut_pay(sudden, cluster_data[i][j])
                for item in cluster_data[i][j]:
                    print(item)
    return cluster_data, lst

def check_long(lst, commom):
    for i in range(0, len(lst)):
        for j in range(0, len(lst[i])):
            for k in range(0, len(lst[i][j])):
                if len(lst[i][j][k]) >= 15:
                    lst[i][j][k] = lst[i][j][k][:commom]
                lst[i][j][k].insert(0, str(len(lst[i][j][k])))
                print(lst[i][j][k])
    print('checking successfully!')
    return lst

def find_most_frequent(lst):
    filtered_lst = [num for num in lst if num < 15]
    counter = Counter(filtered_lst)
    most_common = counter.most_common(1)
    return most_common[0][0] if most_common else None

