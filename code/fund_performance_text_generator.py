import pandas as pd
import fund_performance_calculator


# 创建基金市场回顾文档
def create_fund_review_document(qdii_last_week_returns, qdii_new_year_returns, qdii_positive_percentage,
                                equity_last_week_returns, equity_new_year_returns, equity_positive_percentage,
                                index_last_week_returns, index_new_year_returns, index_positive_percentage,
                                bond_last_week_returns, bond_new_year_returns, bond_positive_percentage):
    # 添加标题，后面不用，舍弃
    title_text = "基金市场回顾"
    # 添加全市场基金回顾段落
    market_review_text = ""
    # 添加上周收益率段落
    last_week_returns_text = "上周QDII基金、偏股型基金、指数型基金和偏债型基金平均收益率分别为{:.2f}%、{:.2f}%、{:.2f}%、{:.2f}%。".format(
        qdii_last_week_returns * 100, equity_last_week_returns * 100, index_last_week_returns * 100,
        bond_last_week_returns * 100
    )

    # 正收益占比改良版：
    positive_percentage_text = ""
    high_positive_percentage_text = ""
    low_positive_percentage_text = ""
    funds_positive_percentage_text = ""
    funds_positive_percentage = [qdii_positive_percentage, equity_positive_percentage, index_positive_percentage,
                                 bond_positive_percentage]
    counter = 0
    for funds in funds_positive_percentage:
        if funds < 50:
            counter += 1
        else:
            counter = counter
    if counter == 4:
        positive_percentage_text += "上周QDII基金、偏股型基金、指数型基金、偏债型基金的上周正收益占比均低于50%,赚钱效应较弱。"
        funds_positive_percentage_text = positive_percentage_text
    elif 0 < counter < 4:
        low_positive_percentage_text = "上周除了"
        if qdii_positive_percentage < 50:
            low_positive_percentage_text += "QDII基金，"
        else:
            high_positive_percentage_text += "QDII基金，"
        if equity_positive_percentage < 50:
            low_positive_percentage_text += "偏股型基金，"
        else:
            high_positive_percentage_text += "偏股型基金，"
        if index_positive_percentage < 50:
            low_positive_percentage_text += "指数型基金，"
        else:
            high_positive_percentage_text += "指数型基金，"
        if bond_positive_percentage < 50:
            low_positive_percentage_text += "偏债型基金"
        else:
            high_positive_percentage_text += "偏债型基金"

        low_positive_percentage_text += "正收益占比低于50%，赚钱效应较弱。"
        high_positive_percentage_text += "正收益占比高于50%，赚钱效应较强。"
        funds_positive_percentage_text = low_positive_percentage_text + high_positive_percentage_text
        # positive_percentage_text = funds_positive_percentage_text
    elif counter == 0:
        positive_percentage_text += "上周QDII基金、偏股型基金、指数型基金、偏债型基金的正收益占比均高于50%,赚钱效应较强。"
        funds_positive_percentage_text = positive_percentage_text

    # 添加年度收益率段落
    new_year_returns_text = "2023年以来，QDII基金收益率为{:.2f}%，偏股型基金收益率为{:.2f}%，指数型基金收益率为{:.2f}%，偏债型基金收益率为{:.2f}%。".format(
        qdii_new_year_returns * 100, equity_new_year_returns * 100, index_new_year_returns * 100,
        bond_new_year_returns * 100
    )

    # 保存话术文档
    final_text = market_review_text + last_week_returns_text + funds_positive_percentage_text + new_year_returns_text
    print()
    print("基金市场回顾话术已创建。")
    print()
    return final_text

# 创建偏股基金回顾文档
def create_equity_fund_review_document(average_last_week_returns, average_year_returns,
                                       stock_last_week_returns, hybrid_last_week_returns, balanced_last_week_returns):
    # 添加偏股基金回顾标题
    title_text = ""
    # 添加偏股基金回顾段落
    equity_fund_review_text = "偏股型基金上周的平均收益率为{:.2f}%，今年以来平均收益率为{:.2f}%。".format(
        average_last_week_returns * 100, average_year_returns * 100
    )

    # 添加各类型偏股基金上周收益率段落
    stock_returns_text = "普通股票型基金为{:.2f}%".format(stock_last_week_returns * 100)
    hybrid_returns_text = "、偏股混合型基金为{:.2f}%".format(hybrid_last_week_returns * 100)
    balanced_returns_text = "、平衡混合型基金为{:.2f}%。".format(balanced_last_week_returns * 100)

    returns_paragraph = title_text + equity_fund_review_text + "具体来看各类型偏股基金上周收益率："  +\
                        stock_returns_text + hybrid_returns_text + balanced_returns_text

    # 保存话术
    print()
    print()
    print("偏股基金回顾话术已创建。")
    return returns_paragraph

# 创建偏债基金回顾文档
def create_bond_fund_review_document(average_last_week_returns, average_year_returns,
                                     convertible_last_week_returns, secondary_last_week_returns,
                                     hybrid_bond_last_week_returns, bond_last_week_returns,
                                     interest_rate_last_week_returns, pure_bond_last_week_returns):
    # 添加偏债基金回顾标题
    title_text = ""

    # 添加偏债基金回顾段落
    bond_fund_review_text = "偏债型基金上周的平均收益率为{:.2f}%，今年以来平均收益率为{:.2f}%。".format(
        average_last_week_returns * 100, average_year_returns * 100
    )

    # 添加各类型偏债基金上周收益率段落
    convertible_returns_text = "可转债基为{:.2f}%".format(convertible_last_week_returns * 100)
    secondary_returns_text = "、二级债基为{:.2f}%".format(secondary_last_week_returns * 100)
    hybrid_bond_returns_text = "、偏债混合型基金为{:.2f}%".format(hybrid_bond_last_week_returns * 100)
    bond_returns_text = "、普通债券型基金为{:.2f}%".format(bond_last_week_returns * 100)
    interest_rate_returns_text = "、利率债基为{:.2f}%".format(interest_rate_last_week_returns * 100)
    pure_bond_returns_text = "、纯债基为{:.2f}%。".format(pure_bond_last_week_returns * 100)

    returns_paragraph = title_text + "具体来看各类型偏债基金上周收益率：" + convertible_returns_text \
                        + secondary_returns_text + hybrid_bond_returns_text \
                        + bond_returns_text + interest_rate_returns_text + pure_bond_returns_text

    # 保存文档
    print()
    print()
    print("偏债基金回顾话术已创建。")
    print()
    print("话术程序完成")
    print()
    return returns_paragraph