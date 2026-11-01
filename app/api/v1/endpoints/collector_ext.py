from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.collector_sample import CollectorSample
from app.models.lesson_item import LessonItem

router = APIRouter(tags=["Collector Extensions"])


@router.get("/collector/queries")
async def get_collector_queries(db: AsyncSession = Depends(get_db)):
    """Tìm kiếm/liệt kê các nhóm mẫu thu thập."""
    # Trả về danh sách các label hoặc các nhóm truy vấn mẫu phân theo lesson_item
    stmt = select(CollectorSample.label, func.count(CollectorSample.id).label("total_samples")).group_by(CollectorSample.label)
    result = (await db.execute(stmt)).all()
    return [{"label": r[0], "total_samples": r[1]} for r in result]


@router.get("/collector/queries/{query_id}")
async def get_collector_query_detail(query_id: int, db: AsyncSession = Depends(get_db)):
    """Chi tiết nhóm/truy vấn mẫu theo ID mẫu hoặc ID nhóm."""
    sample = await db.get(CollectorSample, query_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Collector sample/query not found")
    return sample


@router.get("/collector/labels")
async def get_collector_labels(db: AsyncSession = Depends(get_db)):
    """Danh sách các nhãn (sign_label từ lesson_items) có thể thu thập."""
    stmt = select(distinct(LessonItem.sign_label)).where(LessonItem.is_active == True)
    result = await db.execute(stmt)
    labels = result.scalars().all()
    return {"available_labels": labels}