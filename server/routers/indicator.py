# coding: utf-8
"""指标路由: /api/indicator

对应 k-training 的 src/app/api/indicator/route.ts
"""
from fastapi import APIRouter, Depends

from server.db import stocking_models, stocking_engine

from server.core.auth import ApiError
from server.core.deps import require_auth
from server.core.serialize import serialize
from server.schemas.requests import IndicatorRequest

router = APIRouter(prefix="/api", tags=["indicator"], dependencies=[Depends(require_auth)])


@router.post("/indicator")
def query_indicator(body: IndicatorRequest):
    indicator_type = body.indicator_type or body.indicatorType or ""
    if not indicator_type:
        raise ApiError(400, {"data": [], "error": "indicator_type is required"})

    start_raw = next(
        (v for v in [body.starttime, body.startTime, body.start_time] if v is not None), None
    )
    end_raw = next(
        (v for v in [body.endtime, body.endTime, body.end_time] if v is not None), None
    )
    if start_raw is None or end_raw is None:
        raise ApiError(400, {"data": [], "error": "starttime/endtime is required"})

    session = stocking_engine.SessionLocal
    try:
        rows = (
            session.query(stocking_models.DailyIndicatorRecord)
            .filter(
                stocking_models.DailyIndicatorRecord.indicator_type == indicator_type,
                stocking_models.DailyIndicatorRecord.date_time >= start_raw,
                stocking_models.DailyIndicatorRecord.date_time <= end_raw,
            )
            .order_by(stocking_models.DailyIndicatorRecord.date_time.asc())
            .all()
        )
        return {"data": [serialize(r) for r in rows]}
    finally:
        session.remove()
