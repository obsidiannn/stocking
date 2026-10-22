# coding: utf-8
"""策略路由: /api/strategy/*

对应 k-training 的 src/app/api/strategy/*
- GET  /api/strategy/dates
- POST /api/strategy/records
- POST /api/strategy/confirm
- POST /api/strategy/user-record
- GET  /api/strategy/snapshot/dates
- POST /api/strategy/snapshot/records
"""
from fastapi import APIRouter, Depends

from server.core.deps import require_auth
from server.schemas.requests import (
    SnapshotRecordsRequest,
    StrategyConfirmRequest,
    StrategyRecordsRequest,
    UserRecordRequest,
)
from server.services.snapshot_service import query_date, query_records_by_snapshot
from server.services.strategy_service import (
    query_date_by_strategy,
    query_records_by_strategy,
)

router = APIRouter(prefix="/api/strategy", tags=["strategy"], dependencies=[Depends(require_auth)])


@router.get("/dates")
def dates(strategy: str = ""):
    data = query_date_by_strategy(strategy)
    return {"data": data}


@router.post("/records")
def records(body: StrategyRecordsRequest):
    data = query_records_by_strategy(body.strategy, body.date, body.excludes)
    return {"data": data}


@router.post("/confirm")
def confirm(body: StrategyConfirmRequest):
    return {"data": {}}


@router.post("/user-record")
def user_record(body: UserRecordRequest):
    return {"data": {}}


@router.get("/snapshot/dates")
def snapshot_dates():
    data = query_date()
    return {"data": data}


@router.post("/snapshot/records")
def snapshot_records(body: SnapshotRecordsRequest):
    data = query_records_by_snapshot(body.level, body.date)
    return {"data": data}
