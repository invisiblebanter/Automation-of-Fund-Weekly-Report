import pandas as pd

def create_etf_review_text(etf_for_excel):
    df = pd.read_pickle(etf_for_excel)
    # 这里是获取前面5个etf
    first_column_info = df.iloc[:, 0]
    second_column_info = df.iloc[:, 1]
    third_column_info = df.iloc[:, 2]
    fourth_column_info = df.iloc[:, 3]
    fifth_column_info = df.iloc[:, 4]

    etf_text = "上周净值涨跌幅前五的权益ETF为{}、{}、{}、{}和{}，涨跌幅从高到低分别为{:.2f}%、{:.2f}%、{:.2f}%、{:.2f}%和{:.2f}%。"\
        .format(df.columns[0], df.columns[1], df.columns[2], df.columns[3], df.columns[4], first_column_info['value_change'][0] * 100,\
                second_column_info['value_change'][0] * 100, third_column_info['value_change'][0] * 100, fourth_column_info['value_change'][0] * 100,\
                fifth_column_info['value_change'][0] * 100)

    print()
    print(etf_text)
    print()
    print("etf部分话术生成成功")
    return etf_text
