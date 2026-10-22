# coding: utf-8
"""板块快照服务: 日期查询、按级别+日期查询记录

对应 k-training 的 src/api/service/snapshot.service.ts
将 daily_industry_snapshot 映射为 StrategyRecordItem 结构
"""
from server.db import stocking_models , stocking_engine


def query_date():
    session = stocking_engine.SessionLocal
    try:
        rows = (
            session.query(stocking_models.DailyIndustrySnapshot.trade_date)
            .filter(stocking_models.DailyIndustrySnapshot.source_from == "dc")
            .distinct()
            .order_by(stocking_models.DailyIndustrySnapshot.trade_date.asc())
            .all()
        )
        return [r[0] for r in rows if r[0] is not None]
    finally:
        session.remove()


def query_records_by_snapshot(level: str, date: str):
    session = stocking_engine.SessionLocal
    try:
        rows = (
            session.query(stocking_models.DailyIndustrySnapshot)
            .filter(
                stocking_models.DailyIndustrySnapshot.level == level,
                stocking_models.DailyIndustrySnapshot.trade_date == date,
            )
            .order_by(
                stocking_models.DailyIndustrySnapshot.leading_pct.desc(),
                stocking_models.DailyIndustrySnapshot.up_num.desc(),
            )
            .all()
        )
        result = []
        for l in rows:
            data_index = "_".join(
                v for v in [l.leading_code, l.trade_date, l.level, l.idx_type] if v
            )
            pct_str = str(l.leading_pct) if l.leading_pct is not None else ""
            code_split = (l.leading_code or "").split(".")
            record = {
                "id": l.id,
                "strategy_date": l.trade_date,
                "strategy_code": l.source_from,
                "stock_code": code_split[0] if len(code_split) > 0 else None,
                "stock_name": l.leading_name,
                "market_code": code_split[1] if len(code_split) > 1 else None,
                "industry_label": l.industry,
                "concept_label": l.concept_code,
                "is_retest": None,
                "total_point": float(l.leading_pct) if l.leading_pct is not None else None,
                "data_index": data_index,
                "total_reason": " | ".join(
                    v for v in [
                        l.industry,
                        l.idx_type,
                        l.level,
                        "up:" + str(l.up_num or 0),
                        "down:" + str(l.down_num or 0),
                        ("pct:" + pct_str) if pct_str else "",
                    ] if v
                ),
                "capital_value": None,
            }
            result.append({
                "record": record,
                "property": {"up_num": l.up_num, "down_num": l.down_num},
            })
        return result
    finally:
        session.remove()
