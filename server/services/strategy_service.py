# coding: utf-8
"""策略服务: 策略日期/记录查询、日内策略保存、用户确认

对应 k-training 的 src/api/service/strategy.service.ts
复用 hikyuu_money 现有的 demo.orm.models (hikyuu_analysis 库)
"""
from server.db import stocking_engine, stocking_models

from server.core.serialize import serialize


def query_date_by_strategy(strategy: str):
    session = stocking_engine.SessionLocal
    try:
        rows = (
            session.query(stocking_models.StrategyRecord.strategy_date)
            .filter(stocking_models.StrategyRecord.strategy_code == strategy)
            .distinct()
            .order_by(stocking_models.StrategyRecord.strategy_date.asc())
            .all()
        )
        return [r[0] for r in rows if r[0] is not None]
    finally:
        session.remove()


def query_records_by_strategy(strategy: str, date: str, excludes):
    session = stocking_engine.SessionLocal
    try:
        records = (
            session.query(stocking_models.StrategyRecord)
            .filter(
                stocking_models.StrategyRecord.strategy_code == strategy,
                stocking_models.StrategyRecord.strategy_date == date,
            )
            .order_by(
                stocking_models.StrategyRecord.total_point.desc(),
                stocking_models.StrategyRecord.capital_value.desc(),
            )
            .all()
        )
        result = []
        if records:
            data_idxes = [r.data_index for r in records if r.data_index]
            props = (
                session.query(stocking_models.StrategyRecordProperty)
                .filter(stocking_models.StrategyRecordProperty.data_index.in_(data_idxes))
                .all()
            )
            prop_map = {p.data_index: p for p in props}
            for r in records:
                prop = prop_map.get(r.data_index)
                result.append({
                    "record": serialize(r),
                    "property": serialize(prop) if prop else None,
                })

        if excludes:
            result = [
                item for item in result
                if not any(
                    e in (item["record"].get("total_reason") or "")
                    for e in excludes
                )
            ]
        return result
    finally:
        session.remove()
