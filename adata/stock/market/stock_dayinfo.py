# -*- coding: utf-8 -*-
"""
@desc: 股票行业
数据来源：1. 百度

@author: lostar01
@time: 2024/03/13
@log: change log
"""

import pandas as pd
# import numpy as np

from adata.common.headers import baidu_headers
from adata.common.utils import requests
from decimal import Decimal


class StockDayInfo(object):
    """
    股票行业
    """
    def __init__(self) -> None:
        super().__init__()

    def get_stock_dayinfo(self, stock_code='002230'):
        """
        获取股票一天的交易数据
        :param trade_date: 交易日期
        :return: 
        """
        return self.__stock_dayinfo_baidu(stock_code)
    
    def get_stock_fund_dayinfo(self, stock_code='00001',stock_name='科大讯飞'):
        """
        获取资金当天的数据
        :param trade_date: 交易日期
        :return: 
        """
        return self.__stock_fund_dayinfo_baidu(stock_code,stock_name)

    def __stock_dayinfo_baidu(self, stock_code):
        """
        获取百度的股票当天的股票数据： 
        web： https://gushitong.baidu.com/stock/ab-002230
        url： https://finance.pae.baidu.com/vapi/v1/getquotation?all=1&srcid=5353&pointType=string&
              group=quotation_minute_ab&market_type=ab&new_Format=1&name=null&finClientType=pc&
              query=002230&code=002230
        :param stock_code: 股票名称
        :return: 股票行业信息
        """
        columns = ['stock_code', 'stock_name','price_limit']
        null_df = pd.DataFrame(data=[], columns=columns)
        # 1.请求接口 url
        api_url = f"https://finance.pae.baidu.com/vapi/v1/getquotation?" \
                  f"all=1&srcid=5353&pointType=string&group=quotation_minute_ab&market_type=ab&" \
                  f"market_type=ab&new_Format=1&name=null&finClientType=pc&query={stock_code}&code={stock_code}"
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
            "open_price": [],   #开盘价
            "pre_close_price": [],    #昨收
            "close_price": [],  #收盘价
            "high_price": [],   #最高价
            "low_price": [],    #最低价
            "change": [],       #涨跌幅
            "increase": [],     #价格变化
            "volume": [],       #成交量
            "turnover_ratio": [],   #换手率
            "amplitude_ratio": [],  #振幅
            "amount": [],           #成交额
            "pe_ratio": [],         #市盈(TTM)
            "bv_ratio": [],         #市净率
            "financing_balance": [],    #融资余额
            "margin_balance": [],       #融券余额
            "capitalization": [],       #总市值
            "total_share_capital": [],  #总股本
            "currency_value": [],       #流通市值
            "circulation_share_capital": []   #流通股本
        }
        try:
            stock_dayinfo = result['pankouinfos']['list']
            for i in range(len(stock_dayinfo)):
                if stock_dayinfo[i]['ename'] == 'open':
                    res_dict['open_price'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'preClose':
                    res_dict['pre_close_price'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'high':
                    res_dict['high_price'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'low':
                    res_dict['low_price'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'priceLimit':
                    res_dict['change'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'volume':
                    res_dict['volume'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'turnoverRatio':
                    res_dict['turnover_ratio'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'amplitudeRatio':
                    res_dict['amplitude_ratio'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'amount':
                    res_dict['amount'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'peratio':
                    res_dict['pe_ratio'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'bvRatio':
                    res_dict['bv_ratio'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'capitalization':
                    res_dict['capitalization'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'totalShareCapital':
                    res_dict['total_share_capital'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'currencyValue':
                    res_dict['currency_value'].append(stock_dayinfo[i]['originValue'])
                elif stock_dayinfo[i]['ename'] == 'circulatingCapital':
                    res_dict['circulation_share_capital'].append(stock_dayinfo[i]['originValue'])
                
            current = result['cur']
            res_dict['close_price'].append(current['price'])
            res_dict['increase'].append(current['increase'])
            res_dict['financing_balance'].append(0)
            res_dict['margin_balance'].append(0)
            
            tag = result['tag_list']
            for t in range(len(tag)):
                if tag[t]['desc'] == '融资融券标的':
                    extlist = str(tag[t]['ext']).split()
                    finbstr = extlist[1].replace('融资余额：', '').replace(':','')
                    if finbstr.__contains__('亿'):
                        findb = Decimal(finbstr.replace('亿','')) * 100000000
                    else:
                        findb = Decimal(finbstr.replace('万','')) * 10000
                    res_dict['financing_balance'][0] = findb
                    margbstr = extlist[2].replace('融券余额：', '').replace(':','')
                    if margbstr.__contains__('亿'):
                        margb = Decimal(margbstr.replace('亿','')) * 100000000
                    else:
                        margb = Decimal(margbstr.replace('万','')) * 10000
                    res_dict['margin_balance'][0] = margb
                
                    
                    
        except KeyError:
            # TODO logger
            return null_df

        # # 4. 封装数据
        result_df = pd.DataFrame(res_dict) #[['开盘价', '收盘价', '最高价', '最低价', '涨跌幅', '价格变化', '成交量', '换手率', '振幅', '成交额', '市盈(TTM)', '市净率', '融资余额', '融券余额', '总市值', '总股本', '流通市值', '流通股本']
        
        return result_df
    
    def __stock_fund_dayinfo_baidu(self, stock_code='002230',stock_name='科大讯飞'):
        """
        获取百度的股票行业数据：当天的资金数据
        web： https://gushitong.baidu.com/stock/ab-002230
        url： https://finance.pae.baidu.com/vapi/v1/fundflow?finance_type=stock&
             fund_flow_type=&type=stock&market=ab&name=科大讯飞&code=002230&
             belongs=stocklevelone&finClientType=pc
        :param stock_code: 股票代码 stock_name  股票名称
        :return: 股票当天的资金信息
        """

        columns = ['stock_code', 'stock_name']
        null_df = pd.DataFrame(data=[], columns=columns)
        # 1.请求接口 url
        api_url = f"https://finance.pae.baidu.com/vapi/v1/fundflow?finance_type=stock&" \
                  f"fund_flow_type=&type=stock&market=ab&name={stock_name}&code={stock_code}&" \
                  f"belongs=stocklevelone&finClientType=pc"
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
            "super_net_turnover": [],    #特大净流入
            "super_turnover_in": [],     #特大流入
            "super_turnover_out": [],    #特大流出
            "super_turnoverin_rate": [],  #特大流入率
            "super_turnoverout_rate": [], #特大流出率
            "large_net_turnover": [],     #大单净流入
            "large_turnover_in": [],      #大单流入
            "large_turnover_out": [],     #大单流出
            "large_turnoverin_rate": [],  #大单流入率
            "large_turnoverout_rate": [], #大单流出率
            "medium_net_turnover": [],     #中单净流入
            "medium_turnover_in": [],      #中单流入
            "medium_turnover_out": [],     #中单流出
            "medium_turnoverin_rate": [],  #中单流入率
            "medium_turnoverout_rate": [], #中单流出率
            "little_net_turnover": [],     #小单净流入
            "little_turnover_in": [],      #小单流入
            "little_turnover_out": [],     #小单流出
            "little_turnoverin_rate": [],  #小单流入率
            "little_turnoverout_rate": [], #小单流出率
            "main_in": [],     #主力流入
            "main_out": [],    #主力流出
            "main_net_in": [], #主力净流入
            "turnoverin_total": [],  #总流入
            "turnoverout_total": [],  #总流出
            "turnovernet_total": [],  #总净流入
            "main_net_total": [],     #主力净流入
            "unit": [],               #单位 

        }

        try:
            fund_flow = result['content']['fundFlowSpread']['result']
            res_dict['super_net_turnover'].append(fund_flow['superGrp']['netTurnover'])
            res_dict['super_turnover_in'].append(fund_flow['superGrp']['turnoverIn'])
            res_dict['super_turnover_out'].append(fund_flow['superGrp']['turnoverOut'])
            res_dict['super_turnoverin_rate'].append(fund_flow['superGrp']['turnoverInRate'])
            res_dict['super_turnoverout_rate'].append(fund_flow['superGrp']['turnoverOutRate'])
            res_dict['large_net_turnover'].append(fund_flow['largeGrp']['netTurnover'])
            res_dict['large_turnover_in'].append(fund_flow['largeGrp']['turnoverIn'])
            res_dict['large_turnover_out'].append(fund_flow['largeGrp']['turnoverOut'])
            res_dict['large_turnoverin_rate'].append(fund_flow['largeGrp']['turnoverInRate'])
            res_dict['large_turnoverout_rate'].append(fund_flow['largeGrp']['turnoverOutRate'])
            res_dict['medium_net_turnover'].append(fund_flow['mediumGrp']['netTurnover'])
            res_dict['medium_turnover_in'].append(fund_flow['mediumGrp']['turnoverIn'])
            res_dict['medium_turnover_out'].append(fund_flow['mediumGrp']['turnoverOut'])
            res_dict['medium_turnoverin_rate'].append(fund_flow['mediumGrp']['turnoverInRate'])
            res_dict['medium_turnoverout_rate'].append(fund_flow['mediumGrp']['turnoverOutRate'])
            res_dict['little_net_turnover'].append(fund_flow['littleGrp']['netTurnover'])
            res_dict['little_turnover_in'].append(fund_flow['littleGrp']['turnoverIn'])
            res_dict['little_turnover_out'].append(fund_flow['littleGrp']['turnoverOut'])
            res_dict['little_turnoverin_rate'].append(fund_flow['littleGrp']['turnoverInRate'])
            res_dict['little_turnoverout_rate'].append(fund_flow['littleGrp']['turnoverOutRate'])
            res_dict['main_in'].append(fund_flow['todayMainFlow']['mainIn'])
            res_dict['main_out'].append(fund_flow['todayMainFlow']['mainOut'])
            res_dict['main_net_in'].append(fund_flow['todayMainFlow']['mainNetIn'])
            res_dict['turnoverin_total'].append(fund_flow['turnoverInTotal'])
            res_dict['turnoverout_total'].append(fund_flow['turnoverOutTotal'])
            res_dict['turnovernet_total'].append(fund_flow['turnoverNetTotal'])
            res_dict['main_net_total'].append(fund_flow['mainNetTotal'])
            res_dict['unit'].append(fund_flow['unit'])
        
        except KeyError:
            # TODO logger

            return null_df
        
        # # 4. 封装数据
        result_df = pd.DataFrame(res_dict)
        
        return result_df



if __name__ == '__main__':
    print(StockDayInfo().get_stock_dayinfo(stock_code='002230'))
    print(StockDayInfo().get_stock_fund_dayinfo(stock_code='002230', stock_name='科大讯飞'))