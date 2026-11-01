from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user_lesson_progress import UserLessonProgress
from app.models.attempt import Attempt
from app.models.attempt_error import AttemptError

router = APIRouter(tags=["History & Progress Extra"])


@router.get("/users/{user_id}/progress/lessons")
async def get_all_lessons_progress(user_id: int, db: AsyncSession = Depends(get_db)):
    """Tiến độ từng bài (tất cả các bài học mà user đã tương tác)."""
    stmt = select(UserLessonProgress).where(UserLessonProgress.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/users/{user_id}/history")
async def get_user_history(user_id: int, db: AsyncSession = Depends(get_db)):
    """Lịch sử học (danh sách các lượt attempt gần đây của user)."""
    stmt = (
        select(Attempt)
        .where(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .limit(50)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/users/{user_id}/signs/{lesson_item_id}/error-history")
async def get_sign_error_history(user_id: int, lesson_item_id: int, db: AsyncSession = Depends(get_db)):
    """Lịch sử lỗi theo ký hiệu cụ thể của user."""
    stmt = (
        select(AttemptError)
        .join(Attempt, Attempt.id == AttemptError.attempt_id)
        .where(Attempt.user_id == user_id, Attempt.lesson_item_id == lesson_item_id)
        .order_by(AttemptError.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()