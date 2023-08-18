import pandas as pd

def stock_market_xml_preprocessing(xml_file):
    try:
        df = pd.read_xml(xml_file)
        df = df.drop(df.columns[0], axis=1)
        df = df.drop(df.columns[0], axis=1)
        df = df.drop(df.index[0])
        df['日期'] = df['日期'].astype(str)
        df['日期'] = df['日期'].apply(lambda x: x[:8])
        df = df.pivot(index='日期', columns='证券名称', values='最新价')
        df = df.rename_axis(None, axis='columns')
        df = df.rename_axis(None, axis='index')
        df.index = pd.to_datetime(df.index).strftime('%Y%m%d')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        date_list_daily = pd.date_range(df.index[0], df.index[-1], freq='d')
        df = df.reindex(date_list_daily).fillna(method='ffill', limit=6)
        # 按照自己想要的顺序排列，一会儿可以知道输出顺序
        df = df[['上证综合指数', '沪深300指数', '创业板指数(价格)', '恒生指数', '标普500指数',\
            '纳斯达克综合指数', '国证1000价值指数', '国证1000成长指数', '上证50指数', '中证1000指数']]

        df.to_pickle(r'../pickle_file/stock_market_ten_index.pickle')
        print()
        print('股市市场回顾数据处理文件导出成功！！！')
        print()
        return df
    except:
        print()
        print('股市市场回顾数据处理文件导出失败！！！')
        print()

def shenwan_index_xml_preprocessing(xml_file):
    try:
        df = pd.read_xml(xml_file)
        df = df.drop(df.columns[0], axis=1)
        df = df.drop(df.columns[0], axis=1)
        df = df.drop(df.index[0])
        df['日期'] = df['日期'].astype(str)
        df['日期'] = df['日期'].apply(lambda x: x[:8])
        df = df.pivot(index='日期', columns='证券名称', values='最新价')
        df = df.rename_axis(None, axis='columns')
        df = df.rename_axis(None, axis='index')
        df.index = pd.to_datetime(df.index).strftime('%Y%m%d')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        date_list_daily = pd.date_range(df.index[0], df.index[-1], freq='d')
        df = df.reindex(date_list_daily).fillna(method='ffill', limit=6)
        df.to_pickle(r'../pickle_file/shenwan_index.pickle')
        print()
        print('股市市场回顾申万指数部分数据处理文件导出成功！！！')
        print()
        return df
    except:
        print()
        print('股市市场回顾申万指数部分数据处理文件导出失败！！！')
        print()