import pandas as pd
import xml.etree.ElementTree as ET
import warnings
warnings.filterwarnings('ignore')

class XmlData:
    def __init__(self, sector, file_path):
        self.sector = sector
        self.file_path = file_path

    # 这个函数是可以直接返回处理好的数据，返回文件类型是dataframe
    def to_final_value_pickle(self):
        try:
            df = pd.read_xml(self.file_path)
            # 因为导出的xml有分别一个column和一个row无效，需去掉
            df = df.drop(df.columns[0], axis=1)
            df = df.drop(df.index[0])
            df = df.drop(df.columns[0], axis=1)
            df['交易日期'] = df['交易日期'].apply(lambda x: x[:10])
            # 删除'column_name'列中值为NULL的行
            column_name = '流通份额'
            df = df.dropna(subset=[column_name])
            columns_to_drop = ['板块代码', '板块名称']
            df = df.drop(columns_to_drop, axis=1)
            df = df.drop_duplicates()
            df['BETA代码'] = df['BETA代码'] + df['证券名称']
            df = df.pivot(index='交易日期', columns='BETA代码', values='涨跌幅')
            df = df.rename_axis(None, axis='columns')
            df = df.rename_axis(None, axis='index')
            df.index = pd.to_datetime(df.index).strftime('%Y%m%d')
            df = df.astype(float)
            # 数据库中数据为百分数去掉百分号
            df = df / 100
            df = df.sort_index(ascending=True)
            df.index = pd.to_datetime(df.index)
            date_list_daily = pd.date_range(df.index[0], df.index[-1], freq='d')
            df = df.reindex(date_list_daily).fillna(0)
            df.to_pickle(f'../pickle_file/{self.sector}_value.pickle')
            print()
            print(f'{self.sector}_value.pickle生成成功')
            print()
        except:
            print()
            print(f'{self.sector}_value.pickle生成失败')
            print()

    def to_final_portion_pickle(self):
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            data = []

            for child in root:
                row = {}
                for subchild in child:
                    row[subchild.tag] = subchild.text
                data.append(row)
            df = pd.DataFrame(data)
            # 因为导出的xml有分别一个column和一个row无效，需去掉
            df = df.drop(df.columns[0], axis=1)
            df = df.drop(df.index[0])
            df['交易日期'] = df['交易日期'].apply(lambda x: x[:10])
            # 删除'column_name'列中值为NULL的行
            column_name = '流通份额'
            df = df.dropna(subset=[column_name])
            columns_to_drop = ['板块代码', '板块名称']
            df = df.drop(columns_to_drop, axis=1)
            df = df.drop_duplicates()
            df['BETA代码'] = df['BETA代码'] + df['证券名称']
            df = df.pivot(index='交易日期', columns='BETA代码', values='流通份额')
            df = df.rename_axis(None, axis='columns')
            df = df.rename_axis(None, axis='index')
            df.index = pd.to_datetime(df.index).strftime('%Y%m%d')
            df = df.astype(float)
            df = df.sort_index(ascending=True)
            df.index = pd.to_datetime(df.index)
            date_list_daily = pd.date_range(df.index[0], df.index[-1], freq='d')
            df = df.reindex(date_list_daily).fillna(method='ffill', limit=6)
            df.to_pickle(f'../pickle_file/{self.sector}_portion.pickle')
            print()
            print(f'{self.sector}_portion.pickle生成成功')
            print()
        except:
            print()
            print(f'{self.sector}_portion.pickle生成失败')
            print()

    def to_final_portion_compare_pickle(self):
        try:
            df = pd.read_xml(self.file_path)
            # 因为导出的xml有分别一个column和一个row无效，需去掉
            df = df.drop(df.columns[0], axis=1)
            df = df.drop(df.index[0])
            df = df.drop(df.columns[0], axis=1)
            df['交易日期'] = df['交易日期'].apply(lambda x: x[:10])
            # 删除'column_name'列中值为NULL的行
            column_name = '流通份额'
            df = df.dropna(subset=[column_name])
            columns_to_drop = ['板块代码', '板块名称']
            df = df.drop(columns_to_drop, axis=1)
            df = df.drop_duplicates()
            df['BETA代码'] = df['BETA代码'] + df['证券名称']
            df = df.pivot(index='交易日期', columns='BETA代码', values='流通份额')
            df = df.rename_axis(None, axis='columns')
            df = df.rename_axis(None, axis='index')
            df.index = pd.to_datetime(df.index).strftime('%Y%m%d')
            df = df.astype(float)
            df = df.sort_index(ascending=True)
            df.index = pd.to_datetime(df.index)
            date_list_daily = pd.date_range(df.index[0], df.index[-1], freq='d')
            df = df.reindex(date_list_daily).fillna(method='ffill', limit=6)
            df.to_pickle(f'../pickle_file/{self.sector}_portion.pickle')
            print()
            print(f'{self.sector}_portion.pickle生成成功')
            print()
        except:
            print()
            print(f'{self.sector}_portion.pickle生成失败')
            print()