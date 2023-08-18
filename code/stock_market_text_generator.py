import pandas as pd
import stock_market_calculator
import stock_market_data_preprocess

def domestic_stock_market_title_text(data_series):
    up_down_values = data_series[0:10].values * 100
    # 察看市场走向
    if all(value > 0 for value in up_down_values[0:3]):
        market_trend = "普涨"
    elif all(value < 0 for value in up_down_values[0:3]):
        market_trend = "普跌"
    else:
        market_trend = "涨跌互现"

    text = '上周A股市场三大指数{0}'.format(market_trend)
    return text

def shenwan_title_text(data_series):
    positive_count = sum(1 for value in data_series if value > 0)
    negative_count = sum(1 for value in data_series if value < 0)

    if positive_count > negative_count:
        return '，申万31个行业涨多跌少'
    elif positive_count < negative_count:
        return '，申万31个行业涨少跌多'
    else:
        return '，申万31个行业涨跌相当'

def domestic_stock_market_text(data_series):
    up_down_values = data_series[0:10].values * 100
    # 察看市场走向
    if all(value > 0 for value in up_down_values[0:3]):
        market_trend = "普涨"
    elif all(value < 0 for value in up_down_values[0:3]):
        market_trend = "普跌"
    else:
        market_trend = "涨跌互现"

    # 察看风格
    if (up_down_values[6] > up_down_values[7]):
        if (up_down_values[6] > 0 and up_down_values[7] > 0):
            market_style = "价值风格表现优于成长风格，价值指数上涨{0:.2f}%，成长指数上涨{1:.2f}%；".format(up_down_values[6], up_down_values[7])
        elif (up_down_values[6] > 0 and up_down_values[7] < 0):
            market_style = "价值风格表现优于成长风格，价值指数上涨{0:.2f}%，成长指数下跌{1:.2f}%；".format(up_down_values[6], up_down_values[7])
        elif (up_down_values[6] < 0 and up_down_values[7] < 0):
            market_style = "价值风格表现优于成长风格，价值指数下跌{0:.2f}%，成长指数下跌{1:.2f}%；".format(up_down_values[6], up_down_values[7])
    # 基本不可能出现，只是放在这里,同时up down value里面那里可以改为7
    elif (up_down_values[6] == up_down_values[7]):
        market_style = "价值风格和成长风格表现相当，价值指数和成长指数均涨跌为{0:.2f}%；".format(up_down_values[6])
    else:
        if (up_down_values[7] > 0 and up_down_values[6] >0):
            market_style = "成长风格表现优于价值风格，成长指数上涨{0:.2f}%，价值指数上涨{1:.2f}%；".format(up_down_values[7], up_down_values[6])
        elif (up_down_values[7] > 0 and up_down_values[6] < 0):
            market_style = "成长风格表现优于价值风格，成长指数上涨{0:.2f}%，价值指数下跌{1:.2f}%；".format(up_down_values[7], up_down_values[6])
        elif (up_down_values[7] < 0 and up_down_values[6] < 0):
            market_style = "成长风格表现优于价值风格，成长指数下跌{0:.2f}%，价值指数下跌{1:.2f}%；".format(up_down_values[7], up_down_values[6])

    # 查看大小盘
    if  (up_down_values[8] > up_down_values[9]):
        if (up_down_values[8] > 0 and up_down_values[9] > 0):
            market_cap = "大盘风格表现优于小盘风格，大盘指数上涨{0:.2f}%，小盘指数上涨{1:.2f}%。".format(up_down_values[8], up_down_values[9])
        elif (up_down_values[8] > 0 and up_down_values[9] < 0):
            market_cap = "大盘风格表现优于小盘风格，大盘指数上涨{0:.2f}%，小盘指数下跌{1:.2f}%。".format(up_down_values[8], up_down_values[9])
        elif (up_down_values[8] < 0 and up_down_values[9] < 0):
            market_cap = "大盘风格表现优于小盘风格，大盘指数下跌{0:.2f}%，小盘指数下跌{1:.2f}%。".format(up_down_values[8], up_down_values[9])
    # 道理同上
    elif (up_down_values[8] == up_down_values[9]):
        market_cap = "大盘和小盘表现相当，他们的涨跌幅均为{0:.2f}%。".format(up_down_values[8])
    else:
        if (up_down_values[9] > 0 and up_down_values[8] > 0):
            market_cap = "小盘风格表现优于大盘风格，小盘指数上涨{0:.2f}%，大盘指数上涨{1:.2f}%。".format(up_down_values[9], up_down_values[8])
        elif (up_down_values[9] > 0 and up_down_values[8] < 0):
            market_cap = "小盘风格表现优于大盘风格，小盘指数上涨{0:.2f}%，大盘指数下跌{1:.2f}%。".format(up_down_values[9], up_down_values[8])
        elif (up_down_values[9] < 0 and up_down_values[8] < 0):
            market_cap = "小盘风格表现优于大盘风格，小盘指数下跌{0:.2f}%，大盘指数下跌{1:.2f}%。".format(up_down_values[9], up_down_values[8])

    template_1 = '上周A股市场三大指数{0}，上证指数收于{1}。具体来看，上证指数、沪深300和创业板指周涨跌幅分别为{2:.2f}%、{3:.2f}%、{4:.2f}%。市场风格方面，'
    template_1 = template_1.format(market_trend, data_series[-1], up_down_values[0], up_down_values[1], up_down_values[2])
    template_2 = market_style
    template_3 = market_cap
    result = template_1 + template_2 + template_3
    return result

def oversea_stock_market_text(data_series):
    up_down_values = data_series[3:6].values * 100
    if all(value > 0 for value in up_down_values[0:3]):
        market_trend = "普涨"
    elif all(value < 0 for value in up_down_values[0:3]):
        market_trend = "普跌"
    else:
        market_trend = "涨跌互现"
    oversea_index_text = "海外股市：上周海外股市{0}。具体来看，恒生指数、标普500、纳斯达克指数周涨跌幅分别为{1:.2f}%、{2:.2f}%、{3:.2f}%。"\
        .format(market_trend, up_down_values[0], up_down_values[1], up_down_values[2])
    return oversea_index_text

def shenwan_text(data_series):
    data = data_series.values * 100
    shenwan_text_ahead = "行业方面，申万31个行业中，{0}({1:.2f}%)、{2}({3:.2f}%)、{4}({5:.2f}%)、{6}({7:.2f}%)、{8}({9:.2f}%)表现相对靠前；"\
        .format(data_series.index[0],data[0],data_series.index[1],data[1],data_series.index[2],\
                data[2],data_series.index[3],data[3],data_series.index[4],data[4])
    shenwan_text_back = "{0}({1:.2f}%)、{2}({3:.2f}%)、{4}({5:.2f}%)、{6}({7:.2f}%)、{8}({9:.2f}%)表现相对落后。"\
        .format(data_series.index[26],data[26],data_series.index[27],data[27],data_series.index[28],data[28],\
            data_series.index[29],data[29],data_series.index[30],data[30])
    shenwan_text = shenwan_text_ahead + shenwan_text_back
    return shenwan_text

