# -*- coding: utf-8 -*-
import adata

if __name__ == '__main__':
    print(adata.version())
    # 代理
    adata.proxy(False)

    # 分红派息
    # df = adata.stock.market.get_dividend(stock_code='002594')
    # print(df)

    # 获取股票
    # res_df = adata.stock.info.all_code()
    # print(res_df)

    # k_type: k线类型：1.日；2.周；3.月 默认：1 日k
    # res_df = adata.stock.market.get_market(stock_code='000001', k_type=1, start_date='2024-02-28')
    # print(res_df)

    # res_df = adata.stock.market.get_market_min(stock_code='002230')
    # print(res_df)

    res_df = adata.stock.market.get_industry(trade_date='20240303')
    print(res_df)