import pandas as pd
df = pd.read_pickle(r"../pickle_file/主题ETF计算结果.pickle")

"""
处理数据
"""
df = pd.DataFrame(df)
# 根据目标行的信息对列进行重新排序
df = df.sort_values(by='value_change', axis=1, ascending=False)
# differenct sectors单独提取
first_column_info = df.iloc[:, 0]
second_column_info = df.iloc[:, 1]
third_column_info = df.iloc[:, 2]
fourth_column_info = df.iloc[:, 3]
fifth_column_info = df.iloc[:, 4]

"""
写入excel
"""
import openpyxl
excel_file_path = r"../excel_file/ETF_EXCEL.xlsx"
workbook = openpyxl.load_workbook(excel_file_path)

sheet_name = "sheet1"
sheet = workbook[sheet_name]
# 把数据写进去特定的cell

# etf1
sheet["B9"] = first_column_info['calculate_shares_sum'][0]
sheet["B8"] = first_column_info['calculate_shares_sum'][1]
sheet["B7"] = first_column_info['calculate_shares_sum'][2]
sheet["B6"] = first_column_info['calculate_shares_sum'][3]
sheet["C9"] = first_column_info['value_change'][0]
sheet["C8"] = first_column_info['value_change'][1]
sheet["C7"] = first_column_info['value_change'][2]
sheet["C6"] = first_column_info['value_change'][3]
sheet["I6"] = df.columns[0]
sheet['O6'] = first_column_info['top_etf'][0][:9]
sheet['O7'] = first_column_info['top_etf'][1][:9]
sheet['O8'] = first_column_info['top_etf'][2][:9]
sheet['P6'] = first_column_info['top_etf'][0][9:]
sheet['P7'] = first_column_info['top_etf'][1][9:]
sheet['P8'] = first_column_info['top_etf'][2][9:]
# etf2
sheet["B15"] = second_column_info['calculate_shares_sum'][0]
sheet["B14"] = second_column_info['calculate_shares_sum'][1]
sheet["B13"] = second_column_info['calculate_shares_sum'][2]
sheet["B12"] = second_column_info['calculate_shares_sum'][3]
sheet["C15"] = second_column_info['value_change'][0]
sheet["C14"] = second_column_info['value_change'][1]
sheet["C13"] = second_column_info['value_change'][2]
sheet["C12"] = second_column_info['value_change'][3]
sheet["I9"] = df.columns[1]
sheet['O9'] = second_column_info['top_etf'][0][:9]
sheet['O10'] = second_column_info['top_etf'][1][:9]
sheet['O11'] = second_column_info['top_etf'][2][:9]
sheet['P9'] = second_column_info['top_etf'][0][9:]
sheet['P10'] = second_column_info['top_etf'][1][9:]
sheet['P11'] = second_column_info['top_etf'][2][9:]
# etf3
sheet["B21"] = third_column_info['calculate_shares_sum'][0]
sheet["B20"] = third_column_info['calculate_shares_sum'][1]
sheet["B19"] = third_column_info['calculate_shares_sum'][2]
sheet["B18"] = third_column_info['calculate_shares_sum'][3]
sheet["C21"] = third_column_info['value_change'][0]
sheet["C20"] = third_column_info['value_change'][1]
sheet["C19"] = third_column_info['value_change'][2]
sheet["C18"] = third_column_info['value_change'][3]
sheet["I12"] = df.columns[2]
sheet['O12'] = third_column_info['top_etf'][0][:9]
sheet['O13'] = third_column_info['top_etf'][1][:9]
sheet['O14'] = third_column_info['top_etf'][2][:9]
sheet['P12'] = third_column_info['top_etf'][0][9:]
sheet['P13'] = third_column_info['top_etf'][1][9:]
sheet['P14'] = third_column_info['top_etf'][2][9:]
# etf4
sheet["F9"] = fourth_column_info['calculate_shares_sum'][0]
sheet["F8"] = fourth_column_info['calculate_shares_sum'][1]
sheet["F7"] = fourth_column_info['calculate_shares_sum'][2]
sheet["F6"] = fourth_column_info['calculate_shares_sum'][3]
sheet["G9"] = fourth_column_info['value_change'][0]
sheet["G8"] = fourth_column_info['value_change'][1]
sheet["G7"] = fourth_column_info['value_change'][2]
sheet["G6"] = fourth_column_info['value_change'][3]
sheet["I15"] = df.columns[3]
sheet['O15'] = fourth_column_info['top_etf'][0][:9]
sheet['O16'] = fourth_column_info['top_etf'][1][:9]
sheet['O17'] = fourth_column_info['top_etf'][2][:9]
sheet['P15'] = fourth_column_info['top_etf'][0][9:]
sheet['P16'] = fourth_column_info['top_etf'][1][9:]
sheet['P17'] = fourth_column_info['top_etf'][2][9:]
# etf5
sheet["F15"] = fifth_column_info['calculate_shares_sum'][0]
sheet["F14"] = fifth_column_info['calculate_shares_sum'][1]
sheet["F13"] = fifth_column_info['calculate_shares_sum'][2]
sheet["F12"] = fifth_column_info['calculate_shares_sum'][3]
sheet["G15"] = fifth_column_info['value_change'][0]
sheet["G14"] = fifth_column_info['value_change'][1]
sheet["G13"] = fifth_column_info['value_change'][2]
sheet["G12"] = fifth_column_info['value_change'][3]
sheet["I18"] = df.columns[4]
sheet['O18'] = fifth_column_info['top_etf'][0][:9]
sheet['O19'] = fifth_column_info['top_etf'][1][:9]
sheet['O20'] = fifth_column_info['top_etf'][2][:9]
sheet['P18'] = fifth_column_info['top_etf'][0][9:]
sheet['P19'] = fifth_column_info['top_etf'][1][9:]
sheet['P20'] = fifth_column_info['top_etf'][2][9:]


"""
输出
"""
output_file_path = r"../excel_file/截图用.xlsx"
workbook.save(output_file_path)
