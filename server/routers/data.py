# coding: utf-8
"""K线数据路由: /api/data | /api/data/min5

对应 k-training 的 src/app/api/data/*
"""
from fastapi import APIRouter, Depends

from server.core.deps import require_auth
from server.schemas.requests import DayKlineRequest, Min5KlineRequest
from server.services.kline_service import query_day_kline, query_min5_kline

router = APIRouter(
    prefix="/api", tags=["data"], dependencies=[Depends(require_auth)])


@router.post("/data")
def day_kline(body: DayKlineRequest):
    data = query_day_kline(body.market, body.stockCode, body.date, body.offset)
    return {"data": data}


@router.post("/data/min5")
def min5_kline(body: Min5KlineRequest):
    data = query_min5_kline(body.market, body.stockCode,
                            body.start, body.end, body.offset)
    return {"data": data}
