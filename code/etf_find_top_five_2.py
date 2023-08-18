import pandas as pd
import pickle

df = pd.read_pickle(r'../pickle_file/主题ETF计算结果.pickle')
"""
以下数据为测试用：造假，最后删掉即可
"""
# df['大数据']['calculate_shares_sum'][0] = 6000000000
# df['军工']['calculate_shares_sum'][0] = 6000000000
# df['光伏']['calculate_shares_sum'][0] = 6000000000
# df['芯片半导体']['calculate_shares_sum'][0] = 6000000000
# df['消费']['calculate_shares_sum'][0] = 6000000000
# df['食品饮料']['calculate_shares_sum'][0] = 6000000000

# 所有sector的所有数据
sectors_data  = df
# 下面存放输出结果
selected_sectors = []

# 走遍所有元素
for sector, data in sectors_data.items():
    # 看看有没有超过50亿
    if data['calculate_shares_sum'][0] > 5000000000:
        # 第一个数就是上周净值涨幅
        value_change = data['value_change'][0]
        # 这些是符合要求的板块
        selected_sectors.append((sector, value_change))

# 排序
selected_sectors.sort(key=lambda x: x[1], reverse=True)

# 初始化
top_5_sectors = []

# 找top5
for sector, value_change in selected_sectors:
    # check if the sector is "食品饮料" and "消费" is already in the top 5
    # 跳过 '食品饮料'
    if sector == "食品饮料" and "消费" in top_5_sectors:
        continue
    # append process for sectors qualified
    top_5_sectors.append(sector)
    # stop when the qualified sectors num reach 5
    if len(top_5_sectors) == 5:
        break

# initialize the output dict
final_sectors = {}

# populate the final_sectors dict with the selected top 5 sectors' data
for sector in top_5_sectors:
    final_sectors[sector] = sectors_data[sector]

# 注意此处还没有排序
final_sectors = pd.DataFrame(final_sectors)
final_sectors = final_sectors.sort_values(by='value_change', axis=1, ascending=False)
# 保存的新路径
output_pickle_file = r'../pickle_file/etf_for_excel.pickle'

# store 'final_sectors' in the new pickle file
with open(output_pickle_file, 'wb') as f:
    pickle.dump(final_sectors, f)

print()
print('*' * 300)
print("输入excel的信息已经被存在pickle文件里面:", output_pickle_file)
print('*' * 300)
print()