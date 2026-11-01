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
    """Đọc chế độ feedback hiện tại từ app_settings."""
    setting = (await db.execute(select(AppSettings).where(AppSettings.setting_key == "feedback_mode"))).scalar_one_or_none()
    return {"feedback_mode": setting.setting_value if setting else {"mode": "adaptive"}}


@router.put("/settings/feedback-mode")
async def update_feedback_mode(payload: FeedbackModeUpdate, db: AsyncSession = Depends(get_db)):
    """Đổi chế độ feedback."""
    setting = (await db.execute(select(AppSettings).where(AppSettings.setting_key == "feedback_mode"))).scalar_one_or_none()
    if not setting:
        setting = AppSettings(setting_key="feedback_mode", setting_value={"mode": payload.mode})
        db.add(setting)
    else:
        setting.setting_value = {"mode": payload.mode}
    await db.commit()
    return {"status": "success", "mode": payload.mode}


# --- AI Prediction (Server-side stub) ---
@router.post("/predict")
async def predict_sign(payload: dict):
    """Nhận diện landmarks bằng mô hình AI chạy phía server (nếu có)."""
    # Xử lý gọi AI model (ví dụ: MediaPipe + Classifier) ở đây
    return {
        "status": "recognized",
        "predicted_sign": payload.get("target_sign", "UNKNOWN"),
        "confidence": 0.95,
        "errors": []
    }


# --- Collector ---
@router.post("/collector/samples")
async def create_collector_sample(payload: CollectorSampleCreate, db: AsyncSession = Depends(get_db)):
    """Lưu một mẫu dữ liệu thu thập."""
    sample = CollectorSample(
        lesson_item_id=payload.lesson_item_id,
        user_id=payload.user_id,
        label=payload.label,
        landmarks=payload.landmarks,
        metadata=payload.metadata
    )
    db.add(sample)
    await db.commit()
    return {"status": "success", "id": sample.id}


@router.post("/collector/samples/batch")
async def create_collector_samples_batch(payload: CollectorBatchCreate, db: AsyncSession = Depends(get_db)):
    """Lưu nhiều mẫu thu thập cùng lúc."""
    samples = [
        CollectorSample(
            lesson_item_id=s.lesson_item_id,
            user_id=s.user_id,
            label=s.label,
            landmarks=s.landmarks,
            metadata=s.metadata
        ) for s in payload.samples
    ]
    db.add_all(samples)
    await db.commit()
    return {"status": "success", "count": len(samples)}


@router.get("/collector/statistics")
async def get_collector_statistics(db: AsyncSession = Depends(get_db)):
    """Thống kê tổng số lượng mẫu đã thu thập."""
    total_samples = await db.scalar(select(func.count(CollectorSample.id)))
    return {"total_samples": total_samples or 0}