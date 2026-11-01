from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user_lesson_progress import UserLessonProgress
from app.models.lesson import Lesson
from app.schemas.progress import (
    LessonProgressResponse,
    VersionProgressResponse,
    OverallProgressResponse,
    SingleLessonProgressResponse
)

router = APIRouter(
    prefix="/users/{user_id}/progress",
    tags=["Progress"]
)


# =========================
# RESPONSE SCHEMAS
# =========================



# =========================
# 1. OVERALL PROGRESS
# =========================

@router.get(
    "",
    response_model=OverallProgressResponse,
    summary="Lấy tiến độ tổng quan",
    description="Lấy số bài học đã hoàn thành và điểm trung bình của người dùng.",
    response_description="Thông tin tiến độ tổng quan"
)
async def get_overall_progress(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Lấy tiến độ tổng quan toàn khóa của user."""

    stmt = select(
        func.count(UserLessonProgress.id).label("total"),
        func.sum(
            case(
                (UserLessonProgress.is_completed == True, 1),
                else_=0
            )
        ).label("completed"),
        func.avg(UserLessonProgress.best_score).label("avg_score")
    ).where(
        UserLessonProgress.user_id == user_id
    )

    result = (await db.execute(stmt)).first()

    return {
        "user_id": user_id,
        "completed_lessons": result.completed or 0,
        "average_score": (
            round(float(result.avg_score), 2)
            if result.avg_score is not None else 0.0
        )
    }


# =========================
# 2. VERSION PROGRESS
# =========================

@router.get(
    "/versions/{version_id}",
    response_model=VersionProgressResponse,
    summary="Lấy tiến độ theo phiên bản",
    description="Lấy tổng số bài, số bài hoàn thành, tỷ lệ hoàn thành và tiến độ từng bài học.",
    response_description="Thông tin tiến độ của phiên bản"
)
async def get_version_progress(
    user_id: int,
    version_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Lấy tiến độ tổng quan và chi tiết theo phiên bản."""

    stmt = (
        select(
            Lesson.id.label("lesson_id"),
            UserLessonProgress.is_completed,
            UserLessonProgress.best_score
        )
        .outerjoin(
            UserLessonProgress,
            (UserLessonProgress.lesson_id == Lesson.id)
            & (UserLessonProgress.user_id == user_id)
        )
        .where(
            Lesson.version_id == version_id,
            Lesson.is_active == True
        )
        .order_by(Lesson.order_index)
    )

    rows = (await db.execute(stmt)).all()

    lessons = [
        LessonProgressResponse(
            lesson_id=row.lesson_id,
            is_completed=bool(row.is_completed),
            best_score=(
                float(row.best_score)
                if row.best_score is not None else None
            )
        )
        for row in rows
    ]

    total_lessons = len(lessons)

    completed_lessons = sum(
        1 for lesson in lessons if lesson.is_completed
    )

    completion_percentage = (
        round(completed_lessons / total_lessons * 100, 2)
        if total_lessons > 0 else 0.0
    )

    return VersionProgressResponse(
        user_id=user_id,
        version_id=version_id,
        total_lessons=total_lessons,
        completed_lessons=completed_lessons,
        completion_percentage=completion_percentage,
        lessons=lessons
    )


# =========================
# 3. SINGLE LESSON PROGRESS
# =========================

@router.get(
    "/lessons/{lesson_id}",
    response_model=SingleLessonProgressResponse,
    summary="Lấy tiến độ chi tiết bài học",
    description="Lấy trạng thái hoàn thành, số lần luyện tập và điểm số của người dùng trong một bài học.",
    response_description="Thông tin tiến độ bài học"
)
async def get_single_lesson_progress(
    user_id: int,
    lesson_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Lấy tiến độ chi tiết của một bài học cụ thể."""

    stmt = select(UserLessonProgress).where(
        UserLessonProgress.user_id == user_id,
        UserLessonProgress.lesson_id == lesson_id
    )

    progress = (await db.execute(stmt)).scalar_one_or_none()

    if not progress:
        return {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "is_completed": False,
            "completed_attempts": 0,
            "total_attempts": 0,
            "best_score": None,
            "last_score": None
        }

    return {
        "user_id": user_id,
        "lesson_id": lesson_id,
        "is_completed": progress.is_completed,
        "completed_attempts": progress.completed_attempts,
        "total_attempts": progress.total_attempts,
        "best_score": progress.best_score,
        "last_score": progress.last_score,
        "completed_at": progress.completed_at
    }
