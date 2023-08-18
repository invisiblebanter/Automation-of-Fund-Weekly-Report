import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import os
import pickle
class ProcessedEtfPickleCalculator:
    def __init__(self, sector, file_path, mode, date):
        self.sector = sector
        self.file_path = file_path
        self.date = date

        if mode == 'shares_change':
            self.calculator_portion_change()

        elif mode == 'value_change':
            self.calculator_value_change()

        elif mode == 'top_etf':
            self.find_top_three_funds()

        elif mode =='calculate_shares_sum':
            self.calculate_shares_sum()

        else:
            raise ValueError("Invalid mode. 请重新输入.")

    # 以下四个函数可以返回份额变化率以及当周份额之和

    def calculator_portion_change(self):
        try:
            df = pd.read_pickle(self.file_path)
            date = pd.to_datetime(self.date)
            # 虽然此处变量为last sunday，但是因为实际上日期可能只能到周五，所以此处实际计算的是上周五日期
            last_sunday = date - pd.DateOffset(days=date.dayofweek + 3)
            # 同理，此处是上上周五，下面亦是同理
            last_last_sunday = last_sunday - pd.DateOffset(weeks=1)
            three_prior_sunday = last_last_sunday - pd.DateOffset(weeks=1)
            four_prior_sunday = three_prior_sunday - pd.DateOffset(weeks=1)
            five_prior_sunday = four_prior_sunday - pd.DateOffset(weeks=1)

            last_sunday_portions = df.loc[last_sunday]
            last_last_sunday_portions = df.loc[last_last_sunday]
            three_prior_sunday_portions = df.loc[three_prior_sunday]
            four_prior_sunday_portions = df.loc[four_prior_sunday]
            five_prior_sunday_portions = df.loc[five_prior_sunday]
            first_week_portion_change = pd.Series(index=df.columns)
            second_week_portion_change = pd.Series(index=df.columns)
            third_week_portion_change = pd.Series(index=df.columns)
            fourth_week_portion_change = pd.Series(index=df.columns)

            # initialize the variable
            last_portion_sum = 0

            for fund in df.columns:
                last_portion = last_sunday_portions[fund]
                last_last_portion = last_last_sunday_portions[fund]
                three_prior_portion = three_prior_sunday_portions[fund]
                four_prior_portion = four_prior_sunday_portions[fund]
                five_prior_portion = five_prior_sunday_portions[fund]

                # 份额求和
                last_portion_sum = last_portion_sum + last_portion

                if pd.isnull(last_portion) or pd.isnull(last_last_portion) or last_last_portion == 0:
                    first_week_portion_change[fund] = np.nan
                else:
                    first_week_portion_change[fund] = (float(last_portion) - float(last_last_portion)) / float(last_last_portion)

                if pd.isnull(last_last_portion) or pd.isnull(three_prior_portion) or three_prior_portion == 0:
                    second_week_portion_change[fund] = np.nan
                else:
                    second_week_portion_change[fund] = (float(last_last_portion) - float(three_prior_portion)) / float(three_prior_portion)

                if pd.isnull(three_prior_portion) or pd.isnull(four_prior_portion) or four_prior_portion == 0:
                    third_week_portion_change[fund] = np.nan
                else:
                    third_week_portion_change[fund] = (float(three_prior_portion) - float(four_prior_portion)) / float(four_prior_portion)

                if pd.isnull(four_prior_portion) or pd.isnull(five_prior_portion) or five_prior_portion == 0:
                    fourth_week_portion_change[fund] = np.nan
                else:
                    fourth_week_portion_change[fund] = (float(four_prior_portion) - float(five_prior_portion)) / float(five_prior_portion)

            # 打印结果以用来测试
            # print()
            # print("日期测试：")
            # print()
            # print("上周五日期:", last_sunday.strftime('%Y-%m-%d'))
            # print("上上周五日期:", last_last_sunday.strftime('%Y-%m-%d'))
            # print()
            first_week_portion_change = first_week_portion_change.mean()
            second_week_portion_change = second_week_portion_change.mean()
            third_week_portion_change = third_week_portion_change.mean()
            fourth_week_portion_change = fourth_week_portion_change.mean()
            final_output = [first_week_portion_change, second_week_portion_change, third_week_portion_change, fourth_week_portion_change]
            print("份额部分计算成功")
            return final_output
        except:
            print("份额部分计算返回失败")

    # 注意return的涨跌幅是，1-"涨跌%"， 即上升3%，则最后为1.03，下跌3%，则最后为0.97

    def calculator_value_change(self):
        try:
            df = pd.read_pickle(self.file_path)
            # 将输入的目标日期转换为datetime类型
            date = pd.to_datetime(self.date)

            # 计算上周一和上周五日期
            start_date = date - pd.Timedelta(days=date.weekday() + 7)
            end_date = date - pd.Timedelta(days=date.weekday() + 3)
            start_date_2 = date - pd.Timedelta(days=date.weekday() + 14)
            end_date_2 = date - pd.Timedelta(days=date.weekday() + 10)
            start_date_3 = date - pd.Timedelta(days=date.weekday() + 21)
            end_date_3 = date - pd.Timedelta(days=date.weekday() + 17)
            start_date_4 = date - pd.Timedelta(days=date.weekday() + 28)
            end_date_4 = date - pd.Timedelta(days=date.weekday() + 24)

            # 切片获取上一周的涨跌幅数据
            last_week_returns = df.loc[start_date:end_date, :]
            two_prior_week_returns = df.loc[start_date_2:end_date_2, :]
            three_prior_week_returns = df.loc[start_date_3:end_date_3, :]
            four_prior_week_returns = df.loc[start_date_4:end_date_4, :]

            # 计算上一周的涨跌幅
            # prod计算涨跌幅的累积乘积
            last_week_return = (1 + last_week_returns).prod()  # 使用prod函数计算涨跌幅的累积乘积
            two_prior_week_return = (1 + two_prior_week_returns).prod()
            three_prior_week_return = (1 + three_prior_week_returns).prod()
            four_prior_week_return = (1 + four_prior_week_returns).prod()

            last_week_return = 1 - last_week_return.mean()
            two_prior_week_return = 1 - two_prior_week_return.mean()
            three_prior_week_return = 1 - three_prior_week_return.mean()
            four_prior_week_return = 1 - four_prior_week_return.mean()
            final_output = [last_week_return, two_prior_week_return, three_prior_week_return, four_prior_week_return]

            # 返回结果
            print()
            print("涨跌幅计算成功")
            print()
            return final_output
        except:
            print()
            print("涨跌幅计算失败")
            print()

    def find_top_three_funds(self):
        try:
            # 将输入的目标日期转换为datetime类型
            date = pd.to_datetime(self.date)
            df = pd.read_pickle(self.file_path)

            # 计算上周五日期
            end_date = date - pd.Timedelta(days=date.weekday() + 3)

            # 找到上一周周日的份额最大的三支基金的基金代码
            top_three_funds = df.loc[end_date].nlargest(3).index.tolist()

            # 这是一组三个数据的list
            print()
            print("代表性ETF寻找成功")
            print()
            print(top_three_funds)
            return top_three_funds

        except:
            print()
            print("代表性ETF寻找失败")
            print()

    def calculate_shares_sum(self):
        try:
            # 将输入的目标日期转换为datetime类型
            date = pd.to_datetime(self.date)
            df = pd.read_pickle(self.file_path)

            # 计算上一周的日期范围
            start_date = date - pd.Timedelta(days=date.weekday() + 7)
            end_date = date - pd.Timedelta(days=date.weekday() + 3)
            start_date_2 = date - pd.Timedelta(days=date.weekday() + 14)
            end_date_2 = date - pd.Timedelta(days=date.weekday() + 10)
            start_date_3 = date - pd.Timedelta(days=date.weekday() + 21)
            end_date_3 = date - pd.Timedelta(days=date.weekday() + 17)
            start_date_4 = date - pd.Timedelta(days=date.weekday() + 28)
            end_date_4 = date - pd.Timedelta(days=date.weekday() + 24)

            # 切片获取上一周的份额数据
            last_week_shares = df.loc[start_date:end_date, :]
            two_week_ago_shares = df.loc[start_date_2:end_date_2, :]
            three_week_ago_shares = df.loc[start_date_3:end_date_3, :]
            four_week_ago_shares = df.loc[start_date_4:end_date_4, :]

            # 计算上一周周日当日所有基金的份额之和
            shares_sum_on_last_sunday = last_week_shares.loc[end_date].sum()
            shares_sum_on_last_two_sunday = two_week_ago_shares.loc[end_date_2].sum()
            shares_sum_on_last_three_sunday = three_week_ago_shares.loc[end_date_3].sum()
            shares_sum_on_last_four_sunday = four_week_ago_shares.loc[end_date_4].sum()

            final_output = [shares_sum_on_last_sunday, shares_sum_on_last_two_sunday,\
                            shares_sum_on_last_three_sunday, shares_sum_on_last_four_sunday]


            print()
            print("计算份额成功")
            print()
            return final_output
        except:
            print()
            print("计算份额失败")
            print()