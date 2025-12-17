import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def matching(data):
    plt.figure(figsize=(8, 6))
    for row in data:
        plt.plot(range(len(row)), row, alpha=0.5, linestyle='--', color='gray')
    plt.title('Line Plot for Each Row')
    plt.xlabel('Index')
    plt.ylabel('Value')
    # plt.show()

    x = []
    y = []
    for i, row in enumerate(data):
        x.extend(range(len(row)))
        y.extend(row)

    consistent_x_values = []
    for i in range(len(data[0])):
        y_values = [row[i] for row in data if len(row) > i]
        if len(set(y_values)) == 1:
            consistent_x_values.append(i)

    significant_x_values = []
    flag = 0
    for i in range(1, len(data[0]) - 1):  # 只检查中间的 x 值，避免越界
        y_values = [row[i] for row in data if len(row) > i]  # 收集x对应的所有y值
        y_values0 = [row[i - 1] for row in data if len(row) > i - 1]
        y_values1 = [row[i + 1] for row in data if len(row) > i + 1]
        if len(y_values) > 1:
            max_val = max(y_values)
            min_val = min(y_values)
            # 判断是否存在明显的局部特征（箭头的尖）
            if max_val - min_val > 0.5:
                for row in data:
                    if len(row) > i + 1 and len(row) > i - 1:
                        if row[i] == min_val and row[i - 1] > row[i] and row[i + 1] > row[i]:   # 极小
                            flag = 1
                        if row[i] == max_val and row[i-1] < row[i] and row[i+1] < row[i] and flag == 1:
                            significant_x_values.append(i)
                            break

    scattered_x_values = []
    for i in consistent_x_values:
        if i > 0 and i < len(data[0]) - 1:
            prev_y_values = [row[i-1] for row in data if len(row) > i-1]
            next_y_values = [row[i+1] for row in data if len(row) > i+1]
            y_values = [row[i] for row in data if len(row) > i]
            if len(set(prev_y_values)) != 1 or len(set(next_y_values)) != 1:
                scattered_x_values.append(i)

# 拟合
    def exponential_func(x, a, b, c):
        return a * np.exp(- (b * x)) + c

    popt, pcov = curve_fit(exponential_func, x, y)


    plt.figure(figsize=(8, 6))
    for row in data:
        plt.plot(range(len(row)), row, alpha=0.5, linestyle='--', color='gray')
    plt.plot(range(len(data[0])), exponential_func(range(len(data[0])), *popt), color='red', label='Fitted Curve')
    plt.title('Line Plot for All Rows and Fitted Curve')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend(loc='upper right')
    # plt.show()
# 拟合end
    return consistent_x_values, significant_x_values, scattered_x_values

