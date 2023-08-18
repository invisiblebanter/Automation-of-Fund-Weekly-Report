import warnings
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import stock_market_calculator
import stock_market_data_preprocess

def stock_market_ten_index_plot(input_series):
    try:
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 设置输入图片的信息
        categories = ['上证指数','沪深300','创业板指','恒生指数','标普500','纳斯达克','国证价值','国证成长','上证50','中证1000']

        values = input_series.values
        fig = plt.figure(figsize=(16, 8)) # 此处可以调整画布尺寸
        gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.05)

        # 第一个子图
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axhline(y=0.55, color='black', linestyle='-', linewidth=2)
        ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)

        ax1.text(0.115, 0.255, '图5 上周海内外股市涨跌幅', fontsize=14, va='center', ha='center')
        plt.axis('off')

        # 第二个子图
        ax = fig.add_subplot(gs[1, :])
        bar_width = 0.35
        bar_positions = np.arange(len(categories))
        color_list = ['steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'steelblue', 'grey', 'grey', 'grey', 'grey']
        bars = plt.bar(bar_positions, values, width=bar_width, label='上周平均收益率', color=color_list)
        ax.set_xticks(bar_positions + bar_width / 2)
        ax.set_xticklabels(categories)
        plt.xticks(fontsize=12)
        plt.xticks(color='black')
        plt.xticks(rotation=0)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                if height >= 0:
                    plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                                 xytext=(0, 8), textcoords='offset points', ha='center', va='bottom')
                else:
                    plt.annotate(f'{height * 100:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                                 xytext=(0, -8), textcoords='offset points', ha='center', va='top')

        autolabel(bars)
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))

        # 在x轴上添加垂直线区分海内外指数
        x_line_position1 = 2.5  # 第三个 bar 后面,注意，不知道后面有没有变化，如有变化，需要调整
        x_line_position2 = 5.5  # 第六个 bar 后面,注意，不知道后面有没有变化，如有变化，需要调整
        ax.axvline(x=x_line_position1, color='grey', linestyle='-', linewidth=0.5)
        ax.axvline(x=x_line_position2, color='grey', linestyle='-', linewidth=0.5)
        # plt.legend()

        # 第三个子图
        ax3 = fig.add_subplot(gs[2, :])
        ax3.axhline(y=1.5, color='black', linestyle='-', linewidth=2)
        ax3.text(0.1, 1.45, '数据来源：iFind', fontsize=14, va='center', ha='center')
        plt.axis('off')

        plot_filename = r'../png_file/海内外股市指数.png'
        plt.savefig(plot_filename, bbox_inches='tight', dpi=600, pad_inches=0.1)
        # plt.show()
        print()
        print("*" * 75)
        print("海内外股市指数chart生成成功！！！")
        print("*" * 75)
        print()
        plt.close()
    except:
        print()
        print("*" * 75)
        print("海内外股市指数chart生成失败！！！")
        print("*" * 75)
        print()


def shenwan_index_plot(input_series):
    try:
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        categories = input_series.index
        values = input_series.values
        fig = plt.figure(figsize=(16, 8))
        gs = GridSpec(3, 1, height_ratios=[1, 10, 1], hspace=0.08)

        # 第一个子图
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axhline(y=0.575, color='black', linestyle='-', linewidth=2)
        ax1.axhline(y=0.05, color='black', linestyle='-', linewidth=2)
        ax1.text(0.09, 0.2577, '图6 上周行业涨跌幅', fontsize=14, va='center', ha='center')  # 添加汉字
        plt.axis('off')

        # 第二个suplot
        ax = fig.add_subplot(gs[1, :])
        bar_width = 0.35
        bar_positions = np.arange(len(categories))
        bars = plt.bar(bar_positions, values, width=bar_width, label='上周平均收益率', color='steelblue')
        # plt.title('上周申万行业指数涨跌幅')
        plt.xticks(bar_positions + bar_width / 2, categories)
        plt.xticks(fontsize=9.5)
        plt.xticks(color='black')
        plt.xticks(rotation = 300)

        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))

        # 第三个子图
        ax3 = fig.add_subplot(gs[2, :])
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=2)
        ax3.text(0.1, -0.3, '数据来源：iFind', fontsize=14, va='center', ha='center')  # 添加汉字
        plt.axis('off')

        plot_filename = r'../png_file/申万行业指数.png'
        plt.savefig(plot_filename, bbox_inches='tight', dpi=600, pad_inches=0.15)
        # plt.show()
        print()
        print("*" * 75)
        print("申万行业指数chart生成成功！！！")
        print("*" * 75)
        print()
        plt.close()
    except:
        print()
        print("*" * 75)
        print("申万行业指数chart生成失败！！！")
        print("*" * 75)
        print()
