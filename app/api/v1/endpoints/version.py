from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.version import Version
from app.models.lesson import Lesson
from app.models.user_lesson_progress import UserLessonProgress

router = APIRouter(prefix="/versions", tags=["Versions"])


@router.get("")
async def get_versions(db: AsyncSession = Depends(get_db)):
    """Danh sách tất cả các phiên bản (versions) hoạt động."""
    result = await db.execute(
        select(Version).where(Version.is_active == True).order_by(Version.order_index)
    )
    return result.scalars().all()


@router.get("/{version_id}/lessons")
async def get_lessons_by_version(
    version_id: int,
    user_id: Optional[int] = Query(None, description="ID người dùng để lấy tiến độ (nếu có)"),
    db: AsyncSession = Depends(get_db),
):
    """Danh sách bài học thuộc version kèm trạng thái của user."""
    stmt = (
        select(Lesson, UserLessonProgress)
        .outerjoin(
            UserLessonProgress,
            (UserLessonProgress.lesson_id == Lesson.id) & (UserLessonProgress.user_id == user_id)
        )
        .where(Lesson.version_id == version_id, Lesson.is_active == True)
        .order_by(Lesson.order_index)
    )
    result = await db.execute(stmt)
    rows = result.all()

    response = []
    for lesson, progress in rows:
        response.append({
            "id": lesson.id,
            "version_id": lesson.version_id,
            "title": lesson.title,
            "description": lesson.description,
            "order_index": lesson.order_index,
            "is_active": lesson.is_active,
            "is_completed": progress.is_completed if progress else False,
            "completed_attempts": progress.completed_attempts if progress else 0,
        })
    return response