import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.table import Table
import numpy as np

def new_fund_data_cleaning(xml_file):
    df = pd.read_xml(xml_file)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.index[0])
    df['认购起始日期'] = df['认购起始日期'].astype(str)
    df['认购截止日期'] = df['认购截止日期'].astype(str)
    df['认购起始日期'] = df['认购起始日期'].apply(lambda x: x[:10])
    df['认购截止日期'] = df['认购截止日期'].apply(lambda x: x[:10])
    df = df.rename(columns={'managers': '基金经理'})
    new_column_order = ['基金代码', '基金简称', '基金经理', '基金管理人', '认购起始日期', '认购截止日期', '基金类型']
    # 根据过往周报顺序排列
    df = df.reindex(columns=new_column_order)
    df['认购起始日期'] = pd.to_datetime(df['认购起始日期']).dt.strftime('%Y/%m/%d')
    df['认购截止日期'] = pd.to_datetime(df['认购截止日期']).dt.strftime('%Y/%m/%d')
    df = df.sort_values(by='基金类型')
    return df

def count_stock_fund(df):
    counter = 0
    for types in df['基金类型']:
        if (types == '普通股票型基金' or types == '偏股混合型基金' or types == '平衡混合型基金'):
           counter +=1
    # print(f"一共有 {counter} 只偏股类型的基金。")
    return counter

def count_bond_fund(df):
    counter = 0
    for types in df['基金类型']:
        if (types == '可转债基' or types == '二级债基' or types == '偏债混合型基金'\
                or types == '普通债券型基金' or types == '利率债基'or types == '纯债基'):
           counter +=1
    # print(f"一共有 {counter} 只偏债类型的基金。")
    return counter

def count_qdii_fund(df):
    qdii_count = df[df['基金类型'].str.contains('QDII')].shape[0]
    # print(f"一共有 {qdii_count} 只QDII类型的基金。")
    return qdii_count

def count_fx_fund(df):
    fx_count = df[df['基金类型'].str.contains('货币型')].shape[0]
    # print(f"一共有 {fx_count} 只货币类型的基金。")
    return fx_count

def count_index_fund(df):
    index_count = df[df['基金类型'].str.contains('指数型')].shape[0]
    # print(f"一共有 {index_count} 只指数类型的基金。")
    return index_count

def count_fof_fund(df):
    fof_count = df[df['基金类型'].str.contains('FOF')].shape[0]
    # print(f"一共有 {fof_count} 只FOF类型的基金。")
    return fof_count


def new_issued_fund_title(df, df_last_week):
    count_all = df.shape[0]
    previous_count_all = df_last_week.shape[0] # 无用变量，可删除，之前做测试用
    if df.shape[0] > df_last_week.shape[0]:
        trend_text = '有所上升'
    elif df.shape[0] < df_last_week.shape[0]:
        trend_text = '有所下降'
    else:
        trend_text = '持平'
    text = f'本周拟新发行基金一共{count_all}只,新基发行热度较上周{trend_text}'
    return text


def new_issued_fund_text(df, df_last_week):
    text_parts = []
    stock_count = count_stock_fund(df)
    if stock_count > 0:
        text_parts.append(f'偏股型基金{stock_count}只')

    bond_count = count_bond_fund(df)
    if bond_count > 0:
        text_parts.append(f'偏债型基金{bond_count}只')

    index_count = count_index_fund(df)
    if index_count > 0:
        text_parts.append(f'指数型基金{index_count}只')

    qdii_count = count_qdii_fund(df)
    if qdii_count > 0:
        text_parts.append(f'QDII基金{qdii_count}只')

    fx_count = count_fx_fund(df)
    if fx_count > 0:
        text_parts.append(f'货币型基金{fx_count}只')

    fof_count = count_fof_fund(df)
    if fof_count > 0:
        text_parts.append(f'FOF基金{fof_count}只')

    # 此处变量后面会被overwrite，测试用
    count_all = stock_count + bond_count + index_count + qdii_count + fx_count + fof_count
    previous_count_all = 0  # 这里需要填入上周的数据

    if df.shape[0] > df_last_week.shape[0]:
        trend_text = '有所上升'
    elif df.shape[0] < df_last_week.shape[0]:
        trend_text = '有所下降'
    else:
        trend_text = '持平'

    count_all = df.shape[0]
    previous_count_all = df_last_week.shape[0]
    text = f'本周全市场拟新发行基金一共{count_all}只（同一基金不同份额只展示一只），发行数量较上周（共{previous_count_all}只）{trend_text}。具体来看，'
    text += '、'.join(text_parts) + '。'

    return text



def new_issued_fund_graph_old(df):
    plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(3, 1, height_ratios=[1, 10, 1])

    # 第一个子图
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhline(y=0.5, color='black', linestyle='-', linewidth=2)
    ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)
    ax1.text(0.2, 0.23, '图4 上周及今年以来偏债基金收益率情况', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 第二个子图（包括table）
    ax2 = fig.add_subplot(gs[1, :])
    table_data = []
    table_data.append(df.columns.tolist())
    for index, row in df.iterrows():
        table_data.append(row.tolist())
    column_widths = [max(map(len, str(col))) for col in zip(*table_data)]  # Added str conversion for length calculation

    table = ax2.table(cellText=table_data, cellLoc='center', loc='center')
    # Setting the first row's background to red and text color to white
    for j in range(len(table_data[0])):
        table[0, j].set_facecolor('red')
        table[0, j].set_text_props(color='white')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    for i, width in enumerate(column_widths):
        table.auto_set_column_width([i])

    table.scale(1, 2)
    ax2.axis('off')

    # 第三个子图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.axhline(y=1, color='black', linestyle='-', linewidth=2)
    ax3.text(0.15, 0.75, '数据来源：BETA基金数据库', fontsize=14, va='center', ha='center')  # 添加汉字
    ax3.axis('off')

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.savefig(r'../png_file/新发基金.png', bbox_inches='tight', pad_inches=0.5)

def new_issued_fund_graph(df):
    plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.02)

    # 第一个子图
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=1)
    ax1.axhline(y=0.4, color='black', linestyle='-', linewidth=1)
    ax1.text(0.1, 0.18, '表2 本周新发基金', fontsize=13, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 第二个子图
    ax = fig.add_subplot(gs[1, :])

    input_df = df
    column_labels = input_df.columns.tolist()
    colColors = ["red"]
    colColors.extend(["red"] * len(column_labels))
    # 单元格颜色
    cell_colors = np.full((input_df.shape[0], input_df.shape[1]), "white")
    # 取消坐标轴
    plt.axis('off')

    table = plt.table(cellText=np.array(input_df),
                      colLabels=column_labels,
                      colColours=colColors,
                      cellLoc='center',
                      rowLoc='center',
                      cellColours=cell_colors,
                      loc="center", bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    column_widths = [max(map(len, str(col))) for col in zip(*input_df.values)]
    for i, width in enumerate(column_widths):
        table.auto_set_column_width([i])

    # 第三个子图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.text(0.13, 0.85, '数据来源：BETA基金数据库', fontsize=13, va='center', ha='center')  # 添加汉字
    plt.axis('off')
    plt.savefig(r'../png_file/新发基金.png', bbox_inches='tight', pad_inches=0.05)
