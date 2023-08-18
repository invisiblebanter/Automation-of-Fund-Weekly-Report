import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def broad_based_index_preprocess(file_path):
    df = pd.read_xml(file_path)
    # designed by the structure of the output data
    # 因为输出xml文件有无用行无用列
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.index[0])
    df['日期'] = df['日期'].astype(str)
    # 此处是处理日期
    df['日期'] = df['日期'].apply(lambda x: x[:10])
    # 韩哥方法pivot
    df = df.sort_values(['日期', '证券名字'])
    df = df.drop_duplicates(['证券名字', '日期'], keep='last')
    df_PE = df.pivot(columns='证券名字', index='日期', values='PE_TTM')
    df_PB = df.pivot(columns='证券名字', index='日期', values='PB')
    return [df_PE, df_PB]

def find_now(df, input_date):
    df = df.loc[input_date]
    return df

def pepb_ratio_percentile(dataframe, target_date):
    # slice需要的日期数据
    historical_data = dataframe.loc[dataframe.index <= target_date]
    # 计算rank
    ranks = historical_data.rank(axis=0, pct=True, method='max')
    # 找到pe ratio历史百分位
    target_percentiles = (ranks.iloc[-1] * 100).round(2)
    # 确保输出按照指数的顺序排列，后面好连接两个dataframe
    target_percentiles = target_percentiles.reindex(dataframe.columns)
    return target_percentiles

def pe_range(pe_ptl):
    pe_ptl = pd.DataFrame(pe_ptl)
    columns = pe_ptl.columns
    def category(value):
        if value < 30:
            return '低估'
        elif value > 70:
            return '高估'
        else:
            return '适中'
    pe_ptl['估值'] = pe_ptl[columns[0]].apply(category)
    return pe_ptl

def broad_based_index_text_head(pe_now, pe_rank, input_date):
    input_date = datetime.strptime(input_date, '%Y-%m-%d')
    input_date = input_date.strftime('%Y年%m月%d日')
    broad_text = "截止{0}，{1}、{2}、{3}、{4}、{5}、{6}、{7}的PE估值倍数（估值分位数）分别为{8}（{9}%）、{10}（{11}%）、{12}（{13}%）、{14}（{15}%）、{16}（{17}%）、{18}（{19}%）、{20}（{21}%）,"\
        .format(input_date, pe_now.index[0], pe_now.index[1], pe_now.index[2], pe_now.index[3], pe_now.index[4], pe_now.index[5], pe_now.index[6],\
                pe_now[0], pe_rank[0], pe_now[1], pe_rank[1], pe_now[2], pe_rank[2], pe_now[3], pe_rank[3],\
                pe_now[4], pe_rank[4], pe_now[5], pe_rank[5], pe_now[6], pe_rank[6])

    return broad_text

def broad_based_index_text_back(pe_range):
    df = pe_range
    # 看看有几种估值情况
    valuation_values = df['估值'].unique()
    # 生成高估、低估和适中的宽基指数列表
    overvalued_indices = df[df['估值'] == '高估'].index.tolist()
    undervalued_indices = df[df['估值'] == '低估'].index.tolist()
    moderate_valuation_indices = df[df['估值'] == '适中'].index.tolist()
    # 根据不同情况生成话术
    if len(valuation_values) == 3:
        phrase = f"其中，位于高估水平的宽基指数有{'、'.join(overvalued_indices)}，位于低估的宽基指数有{'、'.join(undervalued_indices)}，处于适中水平之中的宽基指数有{'、'.join(moderate_valuation_indices)}"
    elif len(valuation_values) == 2:
        if '高估' in valuation_values and '低估' in valuation_values:
            phrase = f"其中，处于高估水平的宽基指数有{'、'.join(overvalued_indices)}，其余的宽基指数均为低估水平"
        elif '高估' in valuation_values and '适中' in valuation_values:
            phrase = f"其中，位于高估水平的宽基指数有{'、'.join(overvalued_indices)}，其余的宽基指数均为适中水平"
        elif '低估' in valuation_values and '适中' in valuation_values:
            phrase = f"其中，位于低估水平的宽基指数有{'、'.join(undervalued_indices)}，其余的宽基指数均为适中水平"
    else:
        valuation_level = valuation_values[0]
        phrase = f"其中，所有的宽基指数均处于{valuation_level}水平"

    return phrase

def broad_index_text_generation(pe_now, pe_rank, input_date, pe_range):
    text_1 = broad_based_index_text_head(pe_now, pe_rank, input_date)
    text_2 = broad_based_index_text_back(pe_range)
    final_text = text_1 + text_2
    return final_text

def broad_index_plot(pe_range, pe_now, pe_rank, pb_now, pb_rank):
    pe_rank = pe_rank / 100
    pb_rank = pb_rank / 100
    plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    headers = ["指数名称", "估值情况", "PE", "PE百分位", "PB", "PB百分位"]
    data = [
        [pe_now.index[0], pe_range["估值"][0], pe_now[0], f"{pe_rank[0]:.2%}", pb_now[0], f"{pb_rank[0]:.2%}"],
        [pe_now.index[1], pe_range["估值"][1], pe_now[1], f"{pe_rank[1]:.2%}", pb_now[1], f"{pb_rank[1]:.2%}"],
        [pe_now.index[2], pe_range["估值"][2], pe_now[2], f"{pe_rank[2]:.2%}", pb_now[2], f"{pb_rank[2]:.2%}"],
        [pe_now.index[3], pe_range["估值"][3], pe_now[3], f"{pe_rank[3]:.2%}", pb_now[3], f"{pb_rank[3]:.2%}"],
        [pe_now.index[4], pe_range["估值"][4], pe_now[4], f"{pe_rank[4]:.2%}", pb_now[4], f"{pb_rank[4]:.2%}"],
        [pe_now.index[5], pe_range["估值"][5], pe_now[5], f"{pe_rank[5]:.2%}", pb_now[5], f"{pb_rank[5]:.2%}"],
        [pe_now.index[6], pe_range["估值"][6], pe_now[6], f"{pe_rank[6]:.2%}", pb_now[6], f"{pb_rank[6]:.2%}"],
    ]
    df = pd.DataFrame(data, columns=headers)
    fig, ax = plt.subplots(figsize=(8, 6))
    table_data = []
    table_data.append(df.columns.tolist())
    for index, row in df.iterrows():
        table_data.append(row.tolist())

    column_widths = [max(map(len, str(col))) for col in zip(*table_data)]  # Added str conversion for length calculation

    table = ax.table(cellText=table_data, cellLoc='center', loc='center')

    # Setting the first row's background to red and text color to white
    for j in range(len(table_data[0])):
        table[0, j].set_facecolor('red')
        table[0, j].set_text_props(color='white')

    table.auto_set_font_size(False)
    table.set_fontsize(20)

    for i, width in enumerate(column_widths):
        table.auto_set_column_width([i])

    table.scale(20, 4)
    ax.axis('off')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.savefig(r'../png_file/宽基指数.png', bbox_inches='tight', pad_inches=0.15)

