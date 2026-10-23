# 文件路径：hello_agent.py

import os
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from server.services import kline_service
from server.schemas.requests import StockIndexItem
from server.hikyuu_init import * 

# 使用 ChatOpenAI 并将 base_url 指向 DeepSeek，这是最直接的接入方式
model = ChatOpenAI(
    model="deepseek-flash",          
    api_key=os.environ["OPENAI_API_KEY"],  
    base_url=os.environ["OPENAI_BASE_URL"],   
)


def get_stock_indices(market: str, code: str) -> list[StockIndexItem]:
    """
        获取股票指数列表
        {
            market_code: 'sz'或'sh' 
            index_code: '000001'
            index_name: '上证指数'
        }
    """

    stock_code = market + code
    stock = sm[stock_code]
    list = []

    list.append(StockIndexItem(market_code='sh',index_code='000001',index_name='上证指数'))
    if market.lower() == 'sz':
        list.append(StockIndexItem(market_code='sz',index_code='399001',index_name='深证成指'))
    # https://hikyuu.readthedocs.io/zh-cn/latest/base/constant.html
    if blockzxb[stock_code].code == stock.code:
        bk = blockzxb.index_stock
        list.append(StockIndexItem(market_code=bk.market,index_code=bk.code,index_name=bk.name))

    if zsbk_sh50[stock_code].code == stock.code:
        bk = zsbk_sh50.index_stock
        list.append(StockIndexItem(market_code=bk.market,index_code=bk.code,index_name=bk.name))

    if zsbk_sh180[stock_code].code == stock.code:
        bk = zsbk_sh180.index_stock
        list.append(StockIndexItem(market_code=bk.market,index_code=bk.code,index_name=bk.name))

    if zsbk_hs300[stock_code].code == stock.code:
        bk = zsbk_hs300.index_stock
        list.append(StockIndexItem(market_code=bk.market,index_code=bk.code,index_name=bk.name))

    if zsbk_zz100[stock_code].code == stock.code:
        bk = zsbk_zz100.index_stock
        list.append(StockIndexItem(market_code=bk.market,index_code=bk.code,index_name=bk.name))

    return list


def query_kline_day(market: str, code: str, strategy_date: str):
    """
        查询日k线 数组 
        market: 'sz'或'sh' 
        code: 股票代码,如 '000034'
        strategy_date: 策略日期, 如 '20260101'
    """
    list = kline_service.query_day_kline(market, code, strategy_date )
    return list.filter(lambda k: int(k["date"]) < int(strategy_date))

def query_kline_week(market: str, code: str,  strategy_date: str):
    """
        查询周k线 数组
        market: 'sz'或'sh' 
        code: 股票代码,如 '000034'
        strategy_date: 策略日期, 如 '20260101'
    """
    list = kline_service.query_week_kline(market, code, strategy_date)
    return list.filter(lambda k: int(k["date"]) < int(strategy_date))

def query_index_day(market: str, code: str,  strategy_date: str):
    """
        查询日k线 指数
        market: 'sz'或'sh' 
        code: 股票代码,如 '000001'
        strategy_date: 策略日期, 如 '20260101'
    """
    list = kline_service.query_day_kline(market, code, strategy_date)
    return list.filter(lambda k: int(k["date"]) < int(strategy_date))

def query_index_week(market: str, code: str,  strategy_date: str):
    """
        查询周k线 指数
        market: 'sz'或'sh' 
        code: 股票代码,如 '000001'
        strategy_date: 策略日期, 如 '20260101'
    """
    list = kline_service.query_week_kline(market, code, strategy_date)
    return list.filter(lambda k: int(k["date"]) < int(strategy_date))


agent = create_deep_agent(
    model=model,
    tools=[query_kline_day, query_kline_week, query_index_day, query_index_week,get_stock_indices ],
    # backend="./resource/agent/",
    # memory="./resource/memory/",
    system_prompt="",
)
