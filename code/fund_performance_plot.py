import warnings
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import fund_performance_calculator


# 四大类基金的收益率情况
def four_category_fund_plot(qdii_last_week_returns, qdii_new_year_returns, \
                            equity_last_week_returns, equity_new_year_returns, \
                            index_last_week_returns, index_new_year_returns, \
                            bond_last_week_returns, bond_new_year_returns):
    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    categories = ['QDII基金', '偏股型基金', '指数型基金', '偏债型基金']
    values1 = [qdii_last_week_returns, equity_last_week_returns, index_last_week_returns, bond_last_week_returns]
    values2 = [qdii_new_year_returns, equity_new_year_returns, index_new_year_returns, bond_new_year_returns]

    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.05)
    # 第一个子图
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhline(y=0.5, color='black', linestyle='-', linewidth=2)
    ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)
    ax1.text(0.14, 0.23, '图1 上周各类型基金收益情况', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 第二个子图
    ax = fig.add_subplot(gs[1, :])
    bar_width = 0.35
    bar_positions1 = np.arange(len(categories))
    bar_positions2 = bar_positions1 + bar_width
    bars1 = plt.bar(bar_positions1, values1, width=bar_width, label='上周平均收益率', color='steelblue')
    bars2 = plt.bar(bar_positions2, values2, width=bar_width, label='今年以来平均收益率', color='grey')
    ax.set_xticks(bar_positions1 + bar_width / 2)
    ax.set_xticklabels(categories, fontsize=14.5)
    plt.xticks(color='black')

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height >= 0:
                plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, 8), textcoords='offset points', ha='center', va='bottom')
            else:
                plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, -8), textcoords='offset points', ha='center', va='top')

    autolabel(bars1)
    autolabel(bars2)

    # 设置纵坐标轴格式为百分比
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    plt.legend()

    # 第三个子图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.axhline(y=1.5, color='black', linestyle='-', linewidth=2)
    # ax3.axhline(y=0.8, color='black', linestyle='-', linewidth=2)
    ax3.text(0.15, 1.45, '数据来源：BETA基金数据库', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # plt.legend(labels=['上周平均收益率', '今年以来平均收益率'])
    plot_filename = r'../png_file/四类基金收益.png'
    plt.savefig(plot_filename, dpi = 600, bbox_inches='tight', pad_inches=0.15)
    # plt.show()
    print("*" * 75)
    print("四类基金收益chart已生成")
    print("*" * 75)
    plt.close()


# 各类型基金正收益占比
def four_category_fund_positive_percentage_plot(qdii_positive_percentage, equity_positive_percentage, \
                                                index_positive_percentage, bond_positive_percentage):
    # 基金名称和正收益占比
    funds = ['偏债型基金', '指数型基金', '偏股型基金', 'QDII基金']
    returns = [bond_positive_percentage, index_positive_percentage, equity_positive_percentage,
               qdii_positive_percentage]

    # 将正收益占比转换为百分数形式
    percentages = returns
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.05)
    # 第一个子图
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhline(y=0.5, color='black', linestyle='-', linewidth=2)
    ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)
    ax1.text(0.15, 0.23, '图2 上周各类型基金正收益占比', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 第二个子图
    ax = fig.add_subplot(gs[1, :])
    # 绘制柱状图
    plt.barh(funds, percentages, color='steelblue', height=0.5)
    ax.set_yticklabels(funds, fontsize=14.5)
    plt.yticks(color='black')

    # 添加百分数标签
    for i, v in enumerate(percentages):
        plt.text(v + 0.5, i, f'{v:.2f}%', color='black', va='center')

    # 设置横坐标轴范围
    plt.xlim(0, 100)

    # 设置横坐标轴为百分数形式
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.xaxis.set_visible(False)
    ax.tick_params(axis='x', which='both', length=0)

    # 第三个子图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.axhline(y=1.5, color='black', linestyle='-', linewidth=2)
    ax3.text(0.15, 1.45, '数据来源：BETA基金数据库', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 显示图表
    # plt.show()
    plot_filename = r'../png_file/四类基金正收益.png'
    plt.savefig(plot_filename, dpi = 600, bbox_inches='tight', pad_inches=0.15)
    print("*" * 75)
    print("四类基金正收益chart已生成")
    print("*" * 75)
    plt.close()


# 上周及今年以来偏股基金收益率情况
def stock_skewed_fund_plot(regular_last_week_returns, regular_new_year_returns, \
                           equity_skewed_last_week_returns, equity_skewed_new_year_returns, \
                           balanced_last_week_returns, balanced_new_year_returns):
    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    categories = ['普通股票型基金', '偏股混合型基金', '平衡混合型基金']
    values1 = [regular_last_week_returns, equity_skewed_last_week_returns, balanced_last_week_returns]
    values2 = [regular_new_year_returns, equity_skewed_new_year_returns, balanced_new_year_returns]

    fig = plt.figure(figsize=(14, 7))
    gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.05)
    # 第一个子图
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhline(y=0.6, color='black', linestyle='-', linewidth=2)
    ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)
    ax1.text(0.17, 0.275, '图4 上周及今年以来偏股基金收益率情况', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 第二个子图
    ax = fig.add_subplot(gs[1, :])
    bar_width = 0.15
    bar_positions1 = np.arange(len(categories))
    bar_positions2 = bar_positions1 + bar_width
    bars1 = plt.bar(bar_positions1, values1, width=bar_width, label='上周平均收益率', color='steelblue')
    bars2 = plt.bar(bar_positions2, values2, width=bar_width, label='今年以来平均收益率', color='grey')

    ax.set_xticks(bar_positions1 + bar_width / 2)
    ax.set_xticklabels(categories, fontsize=12.5)
    plt.xticks(color='black')

    # 此处是把plot上面的数字设置为，在正柱上方，负柱下方
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height >= 0:
                plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, 8), textcoords='offset points', ha='center', va='bottom')
            else:
                plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, -8), textcoords='offset points', ha='center', va='top')

    autolabel(bars1)
    autolabel(bars2)

    # 设置纵坐标轴格式为百分比
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    # 创建图例
    plt.legend()
    # 第三个子图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.axhline(y=1.1, color='black', linestyle='-', linewidth=2)
    # ax3.axhline(y=0.8, color='black', linestyle='-', linewidth=2)
    ax3.text(0.15, 1.05, '数据来源：BETA基金数据库', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    plot_filename = r'../png_file/偏股基金收益.png'
    plt.savefig(plot_filename, dpi = 600, bbox_inches='tight', pad_inches=0.15)
    print("*" * 75)
    print("偏股基金收益chart已生成")
    print("*" * 75)
    plt.close()


# 上周及今年以来偏债基金收益率情况
def bond_skewed_fund_plot(convert_bond_last_week_returns, convert_bond_new_year_returns, \
                          secondary_bond_last_week_returns, secondary_bond_new_year_returns, \
                          bond_skewed_last_week_returns, bond_skewed_new_year_returns, \
                          regular_last_week_returns, regular_new_year_returns, \
                          interest_rate_last_week_returns, interest_rate_new_year_returns, \
                          pure_bond_last_week_returns, pure_bond_new_year_returns):

    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    categories = ['可转债基', '二级债基', '偏债混合型基金', '普通债券型基金', '利率债基', '纯债基']
    values1 = [convert_bond_last_week_returns, secondary_bond_last_week_returns, bond_skewed_last_week_returns, \
               regular_last_week_returns, interest_rate_last_week_returns, pure_bond_last_week_returns]
    values2 = [convert_bond_new_year_returns, secondary_bond_new_year_returns, bond_skewed_new_year_returns, \
               regular_new_year_returns, interest_rate_new_year_returns, pure_bond_new_year_returns]

    fig = plt.figure(figsize=(14, 7))
    gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.05)
    # 第一个子图
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhline(y=0.6, color='black', linestyle='-', linewidth=2)
    ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)
    ax1.text(0.166, 0.278, '图4 上周及今年以来偏债基金收益率情况', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    # 第二个子图
    ax = fig.add_subplot(gs[1, :])
    bar_width = 0.3
    bar_positions1 = np.arange(len(categories))
    bar_positions2 = bar_positions1 + bar_width
    bars1 = plt.bar(bar_positions1, values1, width=bar_width, label='上周平均收益率', color='steelblue')
    bars2 = plt.bar(bar_positions2, values2, width=bar_width, label='今年以来平均收益率', color='grey')

    ax.set_xticks(bar_positions1 + bar_width / 2)
    ax.set_xticklabels(categories, fontsize=12)
    plt.xticks(color='black')
    # 此处与上方同理
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height >= 0:
                plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, 8), textcoords='offset points', ha='center', va='bottom')
            else:
                plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, -8), textcoords='offset points', ha='center', va='top')

    autolabel(bars1)
    autolabel(bars2)

    # 设置纵坐标轴格式为百分比
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    # 创建图例
    plt.legend()

    # 第三个子图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.axhline(y=1.1, color='black', linestyle='-', linewidth=2)
    ax3.text(0.15, 1.05, '数据来源：BETA基金数据库', fontsize=14, va='center', ha='center')  # 添加汉字
    plt.axis('off')

    plot_filename = r'../png_file/偏债基金收益.png'
    plt.savefig(plot_filename, bbox_inches='tight', dpi = 600)
    print("*" * 75)
    print("偏债基金收益chart已生成")
    print("*" * 75)
    plt.close()
