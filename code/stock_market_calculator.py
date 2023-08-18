import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import stock_market_data_preprocess

# 画图需要的计算器
def stock_index_weekly_return_calculator(df, input_date):
    try:
        date = pd.to_datetime(input_date)
        # 找到上周周五的日期，变量名字不变，以下变量名字意义全部同理
        last_sunday = date - pd.DateOffset(days=date.dayofweek + 3)
        # 找到上上周日的日期
        last_last_sunday = last_sunday - pd.DateOffset(weeks=1)
        # 选择上周和上上周的日期所对应的指数
        last_sunday_values = df.loc[last_sunday]
        last_last_sunday_values = df.loc[last_last_sunday]
        # 计算每个指数的上周和上上周之间的收益率
        returns = pd.Series(index=df.columns)
        for index in df.columns:
            last_value = last_sunday_values[index]
            last_last_value = last_last_sunday_values[index]
            if pd.isnull(last_value) or pd.isnull(last_last_value) or last_last_value == 0:
                returns[index] = np.nan
            else:
                returns[index] = (float(last_value) - float(last_last_value)) / float(last_last_value)
        print()
        print('股市市场十个指数周涨跌计算成功！！！')
        print()
        return returns
    except:
        print()
        print('股市市场十个指数周涨跌计算失败！！！')
        print()

 # 生成话术需要的
def stock_index_text_calculator(df, input_date):
    try:
        date = pd.to_datetime(input_date)
        # 找到上周五的日期
        last_sunday = date - pd.DateOffset(days=date.dayofweek + 3)
        # 找到上上周日的日期
        last_last_sunday = last_sunday - pd.DateOffset(weeks=1)
        # 选择上周和上上周的日期所对应的指数
        last_sunday_values = df.loc[last_sunday]
        last_last_sunday_values = df.loc[last_last_sunday]
        # 计算每个指数的上周和上上周之间的收益率
        returns = pd.Series(index=df.columns)
        for index in df.columns:
            last_value = last_sunday_values[index]
            last_last_value = last_last_sunday_values[index]
            if pd.isnull(last_value) or pd.isnull(last_last_value) or last_last_value == 0:
                returns[index] = np.nan
            else:
                returns[index] = (float(last_value) - float(last_last_value)) / float(last_last_value)
        new_data = pd.Series(last_sunday_values['上证综合指数'], index=['上证收盘价'])
        returns = returns.append(new_data)
        print()
        print('股市市场十个指数周涨跌计算成功！！！')
        print()
        return returns
    except:
        print()
        print('股市市场十个指数周涨跌计算失败！！！')
        print()

# 画图需要的计算器
def shenwan_index_weekly_return_calculator(df, input_date):
    try:
        date = pd.to_datetime(input_date)
        # 找到上周日的日期
        last_sunday = date - pd.DateOffset(days=date.dayofweek + 3)
        # 找到上上周日的日期
        last_last_sunday = last_sunday - pd.DateOffset(weeks=1)
        # 选择上周和上上周的日期所对应的指数
        last_sunday_values = df.loc[last_sunday]
        last_last_sunday_values = df.loc[last_last_sunday]
        # 计算每个指数的上周和上上周之间的收益率
        returns = pd.Series(index=df.columns)
        for index in df.columns:
            last_value = last_sunday_values[index]
            last_last_value = last_last_sunday_values[index]
            if pd.isnull(last_value) or pd.isnull(last_last_value) or last_last_value == 0:
                returns[index] = np.nan
            else:
                returns[index] = (float(last_value) - float(last_last_value)) / float(last_last_value)
        returns = returns.sort_values(ascending=False)
        print()
        print('申万行业指数周涨跌计算成功！！！')
        print()
        return returns
    except:
        print()
        print('申万行业指数周涨跌计算失败！！！')
        print()

