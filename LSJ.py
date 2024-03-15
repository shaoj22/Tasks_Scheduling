
import pandas as pd 
import numpy as np
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

def linear_interpolation(input_data):
    # 先将无效的字符串替换为NaN
    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            if not isinstance(input_data[i][j], (int, float)):
                input_data[i][j] = np.nan

    # 将输入的二维列表转换为numpy数组
    data = np.array(input_data, dtype=float)

    # 获取行数和列数
    num_rows, num_cols = data.shape

    # 对每一列进行插值
    for col in range(num_cols):
        # 获取当前列的数据
        current_col = data[:, col]

        # 找到非0值的索引
        non_zero_indices = current_col != 0

        # 如果至少有两个非0值，进行线性插值
        if np.sum(non_zero_indices) >= 2:
            # 创建一个线性插值函数
            x = np.where(non_zero_indices)[0]
            y = current_col[non_zero_indices]
            interp_func = np.poly1d(np.polyfit(x, y, 1))

            # 对0值进行插值
            zero_indices = current_col == 0
            interpolated_values = interp_func(np.where(zero_indices)[0])

            # 将负数值替换为NaN
            interpolated_values[interpolated_values < 0] = -1
            current_col[zero_indices] = interpolated_values

    # 保留3位小数
    data = np.round(data, 3)

    # 将插值后的数据返回为二维列表
    return data.tolist()

# 读取数据
lsy_data = pd.read_excel('lsy_data.xlsx', sheet_name='能耗及碳排数据')
# lsy_data.to_csv('lsy_data.csv', index=False, encoding='utf-8')
# 处理国家code
country_code = []
for index, row in lsy_data.iterrows():
    code = row['code']
    if code not in country_code:
        country_code.append(code)

lsy_data.to_csv('test_data.csv', index=False, encoding='utf-8')
# 处理国家指标
country_data = {}
for index, row in lsy_data.iterrows():
    code = row['code']
    year = row['year']
    if year != 2022 and year != 2023:
        if code not in country_data:
            country_data[code] = []
        row_list = row.iloc[7:61].tolist()
        country_data[code].append(row_list)
# 线性插值
# df1 = pd.DataFrame(country_data[2])
# df1.to_csv('data_1.csv', index=False, encoding='utf-8')
# new_data = linear_interpolation(country_data)

for code in country_data:
    country_data[code] = linear_interpolation(country_data[code])

combined_data = []
# 保存数据
for code in country_data:
    combined_data.extend(country_data[code])
df = pd.DataFrame(combined_data)
df.to_csv('result.csv', index=False, encoding='utf-8')
num = 0
for index, row in lsy_data.iterrows():
    year = row['year']
    if year != 2022 and year != 2023:
        lsy_data.iloc[index, 7:61] = combined_data[num]
        num += 1
print(lsy_data)
lsy_data.to_excel('result_1.xlsx', index=False, encoding='utf-8')







