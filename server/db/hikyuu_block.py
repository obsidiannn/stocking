import sqlite3

from server.hikyuu_init import * 


sqlite_path = hikyuu_config['block']['db']

# 公共连接: check_same_thread=False 允许在 FastAPI 线程池等其它线程中复用
conn = sqlite3.connect(sqlite_path, check_same_thread=False)
conn.row_factory = sqlite3.Row


def query() -> list[dict]:
    """用公共连接执行一条 SQL 并返回 dict 列表

    表结构参考 sqlite_path 指向的 stock.db, 常用的有:
    - Block(id, category, name, market_code): 板块及其成分股
    - BlockIndex(id, category, name, market_code): 指数板块
    - Stock(stockid, marketid, code, name, type, valid, startDate, endDate): 股票列表
    """

    
    params: tuple = ()
    return [dict(row) for row in conn.execute(sql, params)]