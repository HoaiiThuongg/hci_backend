from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.collector_sample import CollectorSample
from app.models.app_settings import AppSettings
from app.schemas.platform import FeedbackModeUpdate, CollectorSampleCreate, CollectorBatchCreate

router = APIRouter(tags=["Settings, AI & Collector"])


# --- Settings ---
@router.get("/settings/feedback-mode")
async def get_feedback_mode(db: AsyncSession = Depends(get_db)):
    """Đọc chế độ feedback hiện tại — trả phẳng {"mode": "fixed" | "adaptive"} khớp contract."""
    setting = (await db.execute(select(AppSettings).where(AppSettings.setting_key == "feedback_mode"))).scalar_one_or_none()
    value = setting.setting_value if setting else {"mode": "adaptive"}
    mode = value.get("mode", "adaptive") if isinstance(value, dict) else str(value)
    return {"mode": mode}


@router.put("/settings/feedback-mode")
async def update_feedback_mode(payload: FeedbackModeUpdate, db: AsyncSession = Depends(get_db)):
    """Đổi chế độ feedback."""
    if payload.mode not in ("fixed", "adaptive"):
        raise HTTPException(status_code=422, detail="mode must be 'fixed' or 'adaptive'")
    setting = (await db.execute(select(AppSettings).where(AppSettings.setting_key == "feedback_mode"))).scalar_one_or_none()
    if not setting:
        setting = AppSettings(setting_key="feedback_mode", setting_value={"mode": payload.mode})
        db.add(setting)
    else:
        setting.setting_value = {"mode": payload.mode}
    await db.commit()
    return {"status": "success", "mode": payload.mode}


# --- Collector ---
@router.post("/collector/samples")
async def create_collector_sample(payload: CollectorSampleCreate, db: AsyncSession = Depends(get_db)):
    """Lưu một mẫu dữ liệu thu thập."""
    sample = CollectorSample(
        lesson_item_id=payload.lesson_item_id,
        user_id=payload.user_id,
        label=payload.label,
        landmarks=payload.landmarks,
        sample_metadata=payload.metadata,
    )
    db.add(sample)
    await db.commit()
    return {"status": "success", "id": sample.id}


@router.post("/collector/samples/batch")
async def create_collector_samples_batch(payload: CollectorBatchCreate, db: AsyncSession = Depends(get_db)):
    """Lưu nhiều mẫu thu thập cùng lúc. Trả về số thành công/thất bại."""
    ok, failed = 0, 0
    for s in payload.samples:
        try:
            db.add(CollectorSample(
                lesson_item_id=s.lesson_item_id,
                user_id=s.user_id,
                label=s.label,
                landmarks=s.landmarks,
                sample_metadata=s.metadata,
            ))
            ok += 1
        except Exception:
            failed += 1
    await db.commit()
    return {"status": "success", "count": ok, "failed": failed}


@router.get("/collector/statistics")
async def get_collector_statistics(db: AsyncSession = Depends(get_db)):
    """Thống kê tổng số mẫu + số mẫu theo nhãn cho màn Collector (S6)."""
    total_samples = await db.scalar(select(func.count(CollectorSample.id)))
    by_label_rows = (
        await db.execute(
            select(CollectorSample.label, func.count(CollectorSample.id))
            .group_by(CollectorSample.label)
        )
    ).all()
    return {
        "total_samples": total_samples or 0,
        "by_label": [{"label": r[0], "count": r[1]} for r in by_label_rows],
    }
