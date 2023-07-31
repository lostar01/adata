# -*- coding: utf-8 -*-
"""
@desc: 新闻&舆情相关的数据
@author: 1nchaos
@time:2023/04/06
@log: 
"""
from adata.sentiment.north_flow import NorthFlow
from adata.sentiment.securities_margin import SecuritiesMargin
from adata.sentiment.stock_lifting import StockLifting


class Sentiment(StockLifting, SecuritiesMargin, NorthFlow):

    def __init__(self) -> None:
        super().__init__()


sentiment = Sentiment()
