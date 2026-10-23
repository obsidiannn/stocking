# coding: utf-8
"""K线服务: 从 HDF5 读取日线/5分钟线

对应 k-training 的 src/api/service/kline.service.ts (h5wasm -> h5py)

HDF5 复合字段顺序 (与 h5wasm to_array 索引一致):
  [0] closePrice  [1] datetime  [2] highPrice  [3] lowPrice
  [4] openPrice   [5] transCount [6] transAmount
价格 /1000, 成交量 /10
"""
from server.hikyuu_init import *
from datetime import datetime, timedelta

# ---- dateutil (对应 src/api/lib/dateutil.ts) ----


def plus_date_label(date_str: str, days: int) -> str:
    d = datetime.strptime(date_str, "%Y%m%d")
    return (d + timedelta(days=days)).strftime("%Y%m%d")


# ---- 转换 ----

def _convert_by_date(k):
    result = []
    for i, d in enumerate(k):
        result.append({
            "date": str(d.datetime.ymd),
            "open": d.open,
            "high": d.high,
            "low": d.low,
            "close": d.close,
            "volume":  d.volume / 10,
            "amount": d.amount,
        })
    return result


def _convert_by_min(k):
    result = []
    for i, d in enumerate(k):
        result.append({
            "date": str(d.datetime.ymdhms),
            "open": d.open,
            "high": d.high,
            "low": d.low,
            "close": d.close,
            "volume": d.volume / 10,
            "amount": d.amount,
        })
    return result


# ---- 查询 ----

def query_day_kline(market: str, stock: str, date: str, offset: int = 0):
    start = plus_date_label(date, -365)
    end = plus_date_label(date, offset)
    k = sm[market +
           stock].get_kdata(Query(start=Datetime(start), end=Datetime(end)))
    return _convert_by_date(k)

def query_week_kline(market: str, stock: str, date: str,offset: int = 0):
    start = plus_date_label(date, -720)
    end = plus_date_label(date, offset)
    k = sm[market +
           stock].get_kdata(Query(start=Datetime(start), end=Datetime(end)),
                                ktype=Query.WEEK
                                )
    return _convert_by_date(k)


def query_min5_kline(market: str, stock: str, start_val: str, end_val: str, offset: int = 0):
    start = plus_date_label(start_val, -offset) + "0935"
    end = plus_date_label(end_val, offset) + "1500"
    print(start, end)
    k_min5 = sm[market + stock].get_kdata(
        Query(start=Datetime(start),
              end=Datetime(end),
              ktype=Query.MIN5
              ))
    return _convert_by_min(k_min5)
