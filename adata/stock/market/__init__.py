# -*- coding: utf-8 -*-
"""
@desc: 行情相关的数据
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from adata.stock.market.concepth_market import StockMarketConcept
from adata.stock.market.index_market.market_index import StockMarketIndex
from adata.stock.market.stock_dividend import StockDividend
from adata.stock.market.stock_market import StockMarket
from adata.stock.market.stock_industry import StockIndustry
from adata.stock.market.stock_dayinfo import StockDayInfo


class Market(StockMarket, StockMarketConcept, StockDividend, StockMarketIndex,StockIndustry,StockDayInfo):

    def __init__(self) -> None:
        super().__init__()


market = Market()
