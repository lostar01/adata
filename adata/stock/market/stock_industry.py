# -*- coding: utf-8 -*-
"""
@desc: 股票行业
数据来源：1. 百度

@author: lostar01
@time: 2024/03/03
@log: change log
"""

import pandas as pd
# import numpy as np

from adata.common.headers import baidu_headers
from adata.common.utils import requests


class StockIndustry(object):
    """
    股票行业
    """
    def __init__(self) -> None:
        super().__init__()

    def get_industry(self, trade_date='20240303'):
        """
        获取当个股票的分红信息
        :param trade_date: 交易日期
        :return: 行业信息
        """
        return self.__industry_baidu(trade_date)
    
    def get_industry_stocks(self,industry_code='280600',industry_name='商用车'):
        """
        获取股票行业下的股票列表
        :param industry_code: 行业代码
        :param industry_name: 行业名称
        :return: 股票列表
        """
        return self.__industry_stocks_baidu(industry_code,industry_name)


    def __industry_baidu(self, trade_date):
        """
        获取百度的股票行业数据：交易所；行业板块代码；行业名称；涨跌幅
        web： https://gushitong.baidu.com/blocklist/ab-HY
        url： https://finance.pae.baidu.com/vapi/v2/blocks?
        pn=0&rn=20&market=ab&typeCode=HY&finClientType=pc
        :param trade_date: 交易日期
        :return: 股票行业信息
        """
        columns = ['indutory_code', 'indutory_name','indutory_limit']
        null_df = pd.DataFrame(data=[], columns=columns)
        # 1.请求接口 url
        api_url = f"https://finance.pae.baidu.com/vapi/v2/blocks?" \
                  f"pn=0&rn=1000&market=ab&typeCode=HY&finClientType=pc"
        res = requests.request('get', api_url, headers=baidu_headers.json_headers)

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame()
        
        res_json = res.json()
       
        if str(res_json['ResultCode']) != '0':
            return null_df
        # 3.解析数据
        # 3.1 空数据时返回为空
        result = res_json['Result']
        if not result:
            return null_df
        

        # 3.2 正常解析数据
        res_dict = {
            "market": [],
            "code": [],
            "name": [],
            "ratio": [],
        }
        try:
            for i in range(len(result['blocks'])):
                res_dict['market'].append(result['blocks'][i]['market'])
                res_dict['code'].append(result['blocks'][i]['code'])
                res_dict['name'].append(result['blocks'][i]['name'])
                res_dict['ratio'].append(result['blocks'][i]['ratio']['value'])

        except KeyError:
            # TODO logger
            return null_df
        

        # # 4. 封装数据
        result_df = pd.DataFrame(res_dict) #[['交易所', '行业代码', '行业名称', '涨跌幅']]
        
        return result_df
    
    def __industry_stocks_baidu(self,industry_code,industry_name):
        """
        获取百度的股票行业数据：行业板块代码；板块所属股票
        web： https://gushitong.baidu.com/block/ab-280600
        url： https://gushitong.baidu.com/opendata?resource_id=5352&group=block_stocks&
        finance_type=block&code=280600&finance_type=block&market=ab&marketType=ab&name=%E5%95%86%E7%94%A8%E8%BD%A6&query=280600&pn=0&rn=50&pc_web=1&finClientType=pc
        :param industry_code: 行业代码
        :param industry_name: 行业名称
        :return: 股票信息
        """
        columns = ['stock_code', 'stock_name']
        null_df = pd.DataFrame(data=[], columns=columns)
        # 1.请求接口 url
        api_url = f"https://gushitong.baidu.com/opendata?resource_id=5352&group=block_stocks&" \
                  f"finance_type=block&code={industry_code}&finance_type=block&market=ab&marketType=ab&name={industry_name}&query={industry_code}&pn=0&rn=1000&pc_web=1&finClientType=pc"
        print(api_url)
        res = requests.request('get', api_url, headers=baidu_headers.text_headers)

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame()
        
        res_json = res.json()
       
        if str(res_json['ResultCode']) != '0':
            return null_df
        
        # 3.解析数据
        # 3.1 空数据时返回为空
        result = res_json['Result']
        if not result:
            return null_df

        # 3.2 正常解析数据
        res_dict = {
            "stock_code": [],
            "stock_name": []
        }
        try:
            stock_list = result[0]['DisplayData']['resultData']['tplData']['result']['list']
            
            for i in range(len(stock_list)):
                res_dict['stock_code'].append(stock_list[i]['code'])
                res_dict['stock_name'].append(stock_list[i]['name'])

        except KeyError:
            # TODO logger
            return null_df

        # # 4. 封装数据
        result_df = pd.DataFrame(res_dict) #[['股票代码', '股票名称']]
        
        return result_df
        





if __name__ == '__main__':
    print(StockIndustry().get_industry(trade_date='20240303'))
    print(StockIndustry().get_industry_stocks(industry_code='240400',industry_name='贵金属'))
