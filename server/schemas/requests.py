# coding: utf-8
"""请求体 Pydantic 模型"""
from typing import List, Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str = ""
    password: str = ""


class DayKlineRequest(BaseModel):
    stockCode: str
    date: str
    offset: int = 0
    market: str


class Min5KlineRequest(BaseModel):
    stockCode: str
    start: str
    end: str
    offset: int = 0
    market: str


class IndicatorRequest(BaseModel):
    # 兼容多种字段命名 (indicator_type/indicatorType 等)
    indicator_type: Optional[str] = None
    indicatorType: Optional[str] = None
    starttime: Optional[int] = None
    startTime: Optional[int] = None
    start_time: Optional[int] = None
    endtime: Optional[int] = None
    endTime: Optional[int] = None
    end_time: Optional[int] = None


class StrategyConfirmRequest(BaseModel):
    dataIdx: str
    strategyCode: str


class StrategyRecordsRequest(BaseModel):
    strategy: str = ""
    date: str = ""
    excludes: List[str] = []


class SnapshotRecordsRequest(BaseModel):
    level: str = ""
    date: str = ""


class UserRecordRequest(BaseModel):
    strategy: str = ""
    date: str = ""
