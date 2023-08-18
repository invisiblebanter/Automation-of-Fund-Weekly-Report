import pandas as pd
import numpy as np
import os

# 从sql server提取的数据要进行的处理
def xml_to_pickles(file, newname):
    df = pd.read_xml(file)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.index[0])
    df['截止日期'] = df['截止日期'].apply(lambda x: x[:10])
    filename = f'{newname}.pickle'
    pickle_path = os.path.join("..\pickle_file", filename)
    df.to_pickle(pickle_path)
    print()
    print(f'{pickle_path}合成成功！')
    print()
    return df

def data_cleaning(file_path):
    # 此处file_path其实就是输入dataframe
    df = file_path
    df = df.pivot(index='截止日期', columns='基金代码', values='复权单位净值')
    df = df.rename_axis(None, axis='columns')
    df = df.rename_axis(None, axis='index')
    df.index = pd.to_datetime(df.index).strftime('%Y%m%d')
    df = df.astype(float)
    return df

def refill_df(file_path):
    # 此处file_path其实就是输入dataframe
    # 此处是将日期往后面的日期填充
    df = file_path
    df.index = pd.to_datetime(df.index)
    date_list_daily = pd.date_range(df.index[0], df.index[-1], freq='d')
    df_daily = df.reindex(date_list_daily).fillna(method='ffill', limit=6)
    return df_daily

# 以下为第一个函数，计算上周收益率
def calculate_weekly_returns(dataframe, date):
    # Convert input date to pandas datetime format
    date = pd.to_datetime(date)

    # 找到上周五，因为可能并不能获取周日日期，变量名字不改，只需知道实际是周五日期便可
    last_sunday = date - pd.DateOffset(days=date.dayofweek + 3)

    # 找到上上周五的日期
    last_last_sunday = last_sunday - pd.DateOffset(weeks=1)

    # 选择上周和上上周的日期所对应的基金净值
    last_sunday_values = dataframe.loc[last_sunday]
    last_last_sunday_values = dataframe.loc[last_last_sunday]

    # 计算每个基金的上周和上上周之间的收益率
    returns = pd.Series(index=dataframe.columns)
    for fund in dataframe.columns:
        last_value = last_sunday_values[fund]
        last_last_value = last_last_sunday_values[fund]

        if pd.isnull(last_value) or pd.isnull(last_last_value) or last_last_value == 0:
            returns[fund] = np.nan
        else:
            returns[fund] = (float(last_value) - float(last_last_value)) / float(last_last_value)
    """
    # 打印结果以用来测试
    print("上周日日期:", last_sunday.strftime('%Y-%m-%d'))
    print("上上周日日期:", last_last_sunday.strftime('%Y-%m-%d'))
    """

    return returns

# 以下为第二个函数，计算新年以来收益率
def calculate_returns_last_year(dataframe, input_date):
    # Convert input date to pandas datetime format
    input_date = pd.to_datetime(input_date)

    # 找到去年最后一天的日期，因为前面经过填充，所以大概率可以找到这一天，若是没有，可能需要重新调整，或者直接当成无数据
    last_year_end = pd.to_datetime(str(input_date.year - 1) + '-12-31')

    # 找到他们对应的基金净值
    last_year_values = dataframe.loc[last_year_end]
    input_values = dataframe.loc[input_date]

    # 计算基金收益率
    returns = (input_values - last_year_values) / last_year_values

    """
    # 打印出日期可以去测试
    print("去年最后一天的日期:", last_year_end.strftime('%Y-%m-%d'))
    print("输入的日期:", input_date.strftime('%Y-%m-%d'))
    """

    return returns

# 以下为第三个函数，计算正收益率基金占比
def calculate_positive_return_percentage(returns):
    # 计算收益率为正的基金数量
    positive_returns = returns[returns > 0]
    positive_count = len(positive_returns)

    # 计算收益率为正的基金占比
    total_count = len(returns)
    positive_percentage = positive_count / total_count * 100

    """
    # print out the results
    # 为了好看，我这里直接把他们设成百分数形式
    print("收益率为正的基金占比: {:.2f}%".format(positive_percentage))
    """

    return positive_percentage

# 因为设计算法时的使用的数据模型与实际不符，此处为处理函数

# 这是计算函数！！
def calculate_returns(dataframe, input_date):
    # 调用计算上周收益率的函数
    last_week_returns = calculate_weekly_returns(dataframe, input_date)
    # 调用计算新年以来收益率的函数
    new_year_returns = calculate_returns_last_year(dataframe, input_date)
    return last_week_returns, new_year_returns

# 计算四类基金的正收益率占比
# 读取pickle文件并计算四类基金的收益率及正收益率占比
def calculate_fund_performance(qdii_file, equity_file, index_file, bond_file, input_date):
    # 读取pickle文件并转换为DataFrame
    qdii_dataframe = refill_df(data_cleaning(qdii_file))
    equity_dataframe = refill_df(data_cleaning(equity_file))
    index_dataframe = refill_df(data_cleaning(index_file))
    bond_dataframe = refill_df(data_cleaning(bond_file))

    # 计算四类基金的上周收益率和新年以来收益率
    qdii_last_week_returns, qdii_new_year_returns = calculate_returns(qdii_dataframe, input_date)
    equity_last_week_returns, equity_new_year_returns = calculate_returns(equity_dataframe, input_date)
    index_last_week_returns, index_new_year_returns = calculate_returns(index_dataframe, input_date)
    bond_last_week_returns, bond_new_year_returns = calculate_returns(bond_dataframe, input_date)

    # 计算四类基金的正收益率占比
    qdii_positive_percentage = calculate_positive_return_percentage(qdii_last_week_returns)
    equity_positive_percentage = calculate_positive_return_percentage(equity_last_week_returns)
    index_positive_percentage = calculate_positive_return_percentage(index_last_week_returns)
    bond_positive_percentage = calculate_positive_return_percentage(bond_last_week_returns)

    # 此处要处理结果，否则结果为板块内所有基金的收益率，现在以基金板块为单位计算
    qdii_last_week_returns = qdii_last_week_returns.mean()
    qdii_new_year_returns = qdii_new_year_returns.mean()
    equity_last_week_returns = equity_last_week_returns.mean()
    equity_new_year_returns = equity_new_year_returns.mean()
    index_last_week_returns = index_last_week_returns.mean()
    index_new_year_returns = index_new_year_returns.mean()
    bond_last_week_returns = bond_last_week_returns.mean()
    bond_new_year_returns = bond_new_year_returns.mean()

    # print out结果
    print()
    print("*" * 75)
    print("QDII基金、偏股型基金、指数型基金、偏债型基金本周表现如下：")
    print("*" * 75)

    print()
    print("QDII基金上周收益率: {:.4f}%".format(qdii_last_week_returns * 100))
    # print(qdii_last_week_returns)
    print("QDII基金新年以来收益率: {:.4f}%".format(qdii_new_year_returns * 100))
    # print(qdii_new_year_returns)
    print("QDII基金正收益率占比: {:.4f}%".format(qdii_positive_percentage))
    # print(qdii_positive_percentage)
    print()

    print("偏股型基金上周收益率: {:.4f}%".format(equity_last_week_returns * 100))
    # print(equity_last_week_returns)
    print("偏股型基金新年以来收益率: {:.4f}%".format(equity_new_year_returns * 100))
    # print(equity_new_year_returns)
    print("偏股型基金正收益率占比: {:.4f}%".format(equity_positive_percentage))
    # print(equity_positive_percentage)
    print()

    print("指数型基金上周收益率: {:.4f}%".format(index_last_week_returns * 100))
    # print(index_last_week_returns)
    print("指数型基金新年以来收益率: {:.4f}%".format(index_new_year_returns * 100))
    # print(index_new_year_returns)
    print("指数型基金正收益率占比: {:.4f}%".format(index_positive_percentage))
    print()

    print("偏债型基金上周收益率: {:.4f}%".format(bond_last_week_returns * 100))
    # print(bond_last_week_returns)
    print("偏债型基金新年以来收益率: {:.4f}%".format(bond_new_year_returns * 100))
    # print(bond_new_year_returns)
    print("偏债型基金正收益率占比: {:.4f}%".format(bond_positive_percentage))

    # return the outcome
    return (qdii_last_week_returns, qdii_new_year_returns, qdii_positive_percentage, \
            equity_last_week_returns, equity_new_year_returns, equity_positive_percentage, \
            index_last_week_returns, index_new_year_returns, index_positive_percentage, \
            bond_last_week_returns, bond_new_year_returns, bond_positive_percentage)

"""
股票型基金
"""
# 计算偏股型基金的各种指标，与上述函数一模一样，不过此处换名
# 第一到第四个输入参数分别为 普通股票型基金， 偏股混合型基金， 平衡混合型基金， 输入的日期
def calculate_equity_fund_performance(regular_file, equity_skewed_file, balanced_file, input_date):
    # 读取pickle文件并转换为DataFrame
    regular_dataframe = refill_df(data_cleaning(regular_file))
    equity_skewed_dataframe = refill_df(data_cleaning(equity_skewed_file))
    balanced_dataframe = refill_df(data_cleaning(balanced_file))

    # 计算四类基金的上周收益率和新年以来收益率
    regular_last_week_returns, regular_new_year_returns = calculate_returns(regular_dataframe, input_date)
    equity_skewed_last_week_returns, equity_skewed_new_year_returns = calculate_returns(equity_skewed_dataframe,
                                                                                        input_date)
    balanced_last_week_returns, balanced_new_year_returns = calculate_returns(balanced_dataframe, input_date)

    # 计算四类基金的正收益率占比
    regular_positive_percentage = calculate_positive_return_percentage(regular_last_week_returns)
    equity_skewed_positive_percentage = calculate_positive_return_percentage(equity_skewed_last_week_returns)
    balanced_positive_percentage = calculate_positive_return_percentage(balanced_last_week_returns)

    # 此处要处理结果，否则结果为板块内所有基金的收益率，现在以基金板块为单位计算
    regular_last_week_returns = regular_last_week_returns.mean()
    regular_new_year_returns = regular_new_year_returns.mean()
    equity_skewed_last_week_returns = equity_skewed_last_week_returns.mean()
    equity_skewed_new_year_returns = equity_skewed_new_year_returns.mean()
    balanced_last_week_returns = balanced_last_week_returns.mean()
    balanced_new_year_returns = balanced_new_year_returns.mean()

    # print out结果
    print()
    print("*" * 75)
    print("普通股票型基金、偏股混合型基金、平衡混合型基金本周表现如下：")
    print("*" * 75)

    print()
    print("普通股票型基金上周收益率: {:.4f}%".format(regular_last_week_returns * 100))
    # print(regular_last_week_returns)
    print("普通股票型基金新年以来收益率: {:.4f}%".format(regular_new_year_returns * 100))
    # print(regular_new_year_returns)
    print("普通股票型基金正收益率占比: {:.4f}%".format(regular_positive_percentage))
    print()

    print("偏股混合型基金上周收益率: {:.4f}%".format(equity_skewed_last_week_returns * 100))
    # print(equity_skewed_last_week_returns)
    print("偏股混合型基金新年以来收益率: {:.4f}%".format(equity_skewed_new_year_returns * 100))
    # print(equity_skewed_new_year_returns)
    print("偏股混合型基金正收益率占比: {:.4f}%".format(equity_skewed_positive_percentage))
    print()

    print("平衡混合型基金上周收益率: {:.4f}%".format(balanced_last_week_returns * 100))
    # print(balanced_last_week_returns)
    print("平衡混合型基金新年以来收益率: {:.4f}%".format(balanced_new_year_returns * 100))
    # print(balanced_new_year_returns)
    print("平衡混合型基金正收益率占比: {:.4f}%".format(balanced_positive_percentage))
    print()

    # 输出结果，顺序为普通股票型基金，偏股混合型基金，平衡混合型基金的上周收益率和新年以来收益率还有正收益率占比
    return regular_last_week_returns, regular_new_year_returns, regular_positive_percentage, \
        equity_skewed_last_week_returns, equity_skewed_new_year_returns, equity_skewed_positive_percentage, \
        balanced_last_week_returns, balanced_new_year_returns, balanced_positive_percentage

"""
债券型基金
"""
# 读取pickle文件并计算6类基金的收益率及正收益率占比
# 输入参数从一到七分别是，可转债基金，二级债基金，偏债混合型基金，普通债券型基金，利率债基金，纯债基金，最后为输入日期
def calculate_bond_fund_performance(convert_bond_file, secondary_bond_file, bond_skewed_file, regular_file,
                                    interest_rate_file, pure_bond_file, input_date):
    # 读取pickle文件并转换为DataFrame
    convert_bond_dataframe = refill_df(data_cleaning(convert_bond_file))
    secondary_bond_dataframe = refill_df(data_cleaning(secondary_bond_file))
    bond_skewed_dataframe = refill_df(data_cleaning(bond_skewed_file))
    regular_dataframe = refill_df(data_cleaning(regular_file))
    interest_rate_dataframe = refill_df(data_cleaning(interest_rate_file))
    pure_bond_dataframe = refill_df(data_cleaning(pure_bond_file))

    # 计算四类基金的上周收益率和新年以来收益率
    convert_bond_last_week_returns, convert_bond_new_year_returns = calculate_returns(convert_bond_dataframe,
                                                                                      input_date)
    secondary_bond_last_week_returns, secondary_bond_new_year_returns = calculate_returns(secondary_bond_dataframe,
                                                                                          input_date)
    bond_skewed_last_week_returns, bond_skewed_new_year_returns = calculate_returns(bond_skewed_dataframe, input_date)
    regular_last_week_returns, regular_new_year_returns = calculate_returns(regular_dataframe, input_date)
    interest_rate_last_week_returns, interest_rate_new_year_returns = calculate_returns(interest_rate_dataframe,
                                                                                        input_date)
    pure_bond_last_week_returns, pure_bond_new_year_returns = calculate_returns(pure_bond_dataframe, input_date)

    # 计算四类基金的正收益率占比
    convert_bond_positive_percentage = calculate_positive_return_percentage(convert_bond_last_week_returns)
    secondary_bond_positive_percentage = calculate_positive_return_percentage(secondary_bond_last_week_returns)
    bond_skewed_positive_percentage = calculate_positive_return_percentage(bond_skewed_last_week_returns)
    regular_positive_percentage = calculate_positive_return_percentage(regular_last_week_returns)
    interest_rate_positive_percentage = calculate_positive_return_percentage(interest_rate_last_week_returns)
    pure_bond_positive_percentage = calculate_positive_return_percentage(pure_bond_last_week_returns)

    # 此处要处理结果，否则结果为板块内所有基金的收益率，现在以基金板块为单位计算
    convert_bond_last_week_returns = convert_bond_last_week_returns.mean()
    convert_bond_new_year_returns = convert_bond_new_year_returns.mean()
    secondary_bond_last_week_returns = secondary_bond_last_week_returns.mean()
    secondary_bond_new_year_returns = secondary_bond_new_year_returns.mean()
    bond_skewed_last_week_returns = bond_skewed_last_week_returns.mean()
    bond_skewed_new_year_returns = bond_skewed_new_year_returns.mean()
    regular_last_week_returns = regular_last_week_returns.mean()
    regular_new_year_returns = regular_new_year_returns.mean()
    interest_rate_last_week_returns = interest_rate_last_week_returns.mean()
    interest_rate_new_year_returns = interest_rate_new_year_returns.mean()
    pure_bond_last_week_returns = pure_bond_last_week_returns.mean()
    pure_bond_new_year_returns = pure_bond_new_year_returns.mean()

    # print out结果
    print()
    print("*" * 75)
    print("可转债基金、二极债基金、偏债混合型基金、普通债券型基金、利率债基金、纯债基金本周表现如下：")
    print("*" * 75)

    print()
    print("可转债基金上周收益率: {:.4f}%".format(convert_bond_last_week_returns * 100))
    # print(convert_bond_last_week_returns)
    print("可转债基金新年以来收益率: {:.4f}%".format(convert_bond_new_year_returns * 100))
    # print(convert_bond_new_year_returns)
    print("可转债基金正收益率占比: {:.4f}%".format(convert_bond_positive_percentage))
    print()

    print("二级债基金上周收益率: {:.4f}%".format(secondary_bond_last_week_returns * 100))
    # print(secondary_bond_last_week_returns)
    print("二级债基金新年以来收益率: {:.4f}%".format(secondary_bond_new_year_returns * 100))
    # print(secondary_bond_new_year_returns)
    print("二级债基金正收益率占比: {:.4f}%".format(secondary_bond_positive_percentage))
    print()

    print("偏债混合型基金上周收益率: {:.4f}%".format(bond_skewed_last_week_returns * 100))
    # print(bond_skewed_last_week_returns)
    print("偏债混合型基金新年以来收益率: {:.4f}%".format(bond_skewed_new_year_returns * 100))
    # print(bond_skewed_new_year_returns)
    print("偏债混合型基金正收益率占比: {:.4f}%".format(bond_skewed_positive_percentage))
    print()

    print("普通债券型基金上周收益率: {:.4f}%".format(regular_last_week_returns * 100))
    # print(regular_last_week_returns)
    print("普通债券型基金新年以来收益率: {:.4f}%".format(regular_new_year_returns * 100))
    # print(regular_new_year_returns)
    print("普通债券型基金正收益率占比: {:.4f}%".format(regular_positive_percentage))
    print()

    print("利率债基金上周收益率: {:.4f}%".format(interest_rate_last_week_returns * 100))
    # print(interest_rate_last_week_returns)
    print("利率债基金新年以来收益率: {:.4f}%".format(interest_rate_new_year_returns * 100))
    # print(interest_rate_new_year_returns)
    print("利率债基金正收益率占比: {:.4f}%".format(interest_rate_positive_percentage))
    print()

    print("纯债基金上周收益率: {:.4f}%".format(pure_bond_last_week_returns * 100))
    # print(pure_bond_last_week_returns)
    print("纯债基金新年以来收益率: {:.4f}%".format(pure_bond_new_year_returns * 100))
    # print(pure_bond_new_year_returns)
    print("纯债基金正收益率占比: {:.4f}%".format(pure_bond_positive_percentage))

    # return the outcome
    # 输出结果分别是，可转债基金，二级债基金，偏债混合型基金，普通债券型基金，利率债基金，纯债基金 的上周收益率，新年以来收益率，正收益率占比
    return (convert_bond_last_week_returns, convert_bond_new_year_returns, convert_bond_positive_percentage, \
            secondary_bond_last_week_returns, secondary_bond_new_year_returns, secondary_bond_positive_percentage, \
            bond_skewed_last_week_returns, bond_skewed_new_year_returns, bond_skewed_positive_percentage, \
            regular_last_week_returns, regular_new_year_returns, regular_positive_percentage, \
            interest_rate_last_week_returns, interest_rate_new_year_returns, interest_rate_positive_percentage, \
            pure_bond_last_week_returns, pure_bond_new_year_returns, pure_bond_positive_percentage)