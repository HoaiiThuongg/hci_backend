from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.attempt import Attempt
from app.models.attempt_error import AttemptError
from app.models.feedback import Feedback
from app.models.lesson_item import LessonItem
from app.models.user_lesson_progress import UserLessonProgress
from app.schemas.platform import AttemptCreate, AttemptResponse, LessonSummaryResponse

router = APIRouter(tags=["Attempts & Feedback"])


@router.post("/attempts", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
async def create_attempt(payload: AttemptCreate, db: AsyncSession = Depends(get_db)):
    """Lưu lượt luyện tập (attempt) + attempt_errors + nhãn mức feedback FE đã hiển thị (phương án B)."""
    item = await db.get(LessonItem, payload.lesson_item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson item not found")

    new_attempt = Attempt(
        user_id=payload.user_id,
        lesson_id=payload.lesson_id,
        lesson_item_id=payload.lesson_item_id,
        status=payload.status,
        is_correct=payload.is_correct,
        predicted_sign=payload.predicted_sign,
        model_confidence=payload.model_confidence,
        score=payload.score,
        duration_ms=payload.duration_ms,
        feedback_mode=payload.feedback_mode,
        feedback_level_shown=payload.client_feedback_level,
        is_completed=payload.status == "recognized",
    )
    db.add(new_attempt)
    await db.flush()

    # Lưu lỗi theo 4 tham số — dữ liệu cho error-history + thống kê user study (mục 8.3)
    for err in payload.errors:
        db.add(AttemptError(
            attempt_id=new_attempt.id,
            error_type=err.type,
            severity=err.severity,
            details={"message": err.details} if err.details else None,
        ))

    # Cập nhật progress của user cho bài học
    prog_stmt = select(UserLessonProgress).where(
        UserLessonProgress.user_id == payload.user_id,
        UserLessonProgress.lesson_id == payload.lesson_id,
    )
    progress = (await db.execute(prog_stmt)).scalar_one_or_none()

    if not progress:
        progress = UserLessonProgress(
            user_id=payload.user_id,
            lesson_id=payload.lesson_id,
            total_attempts=1,
            completed_attempts=1 if payload.is_correct else 0,
            last_score=payload.score,
            best_score=payload.score,
            is_completed=False,
        )
        db.add(progress)
    else:
        progress.total_attempts += 1
        if payload.is_correct:
            progress.completed_attempts += 1
        progress.last_score = payload.score
        if payload.score and (progress.best_score is None or payload.score > progress.best_score):
            progress.best_score = payload.score

    await db.commit()
    await db.refresh(new_attempt)
    return new_attempt


@router.get("/attempts/{attempt_id}", response_model=AttemptResponse)
async def get_attempt_detail(attempt_id: int, db: AsyncSession = Depends(get_db)):
    """Chi tiết một lượt luyện."""
    attempt = await db.get(Attempt, attempt_id)
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    return attempt


@router.get("/users/{user_id}/lessons/{lesson_id}/feedback")
async def get_latest_feedback(user_id: int, lesson_id: int, db: AsyncSession = Depends(get_db)):
    """Lấy feedback gần nhất/phù hợp của user trong bài học."""
    stmt = (
        select(Feedback)
        .join(Attempt, Attempt.id == Feedback.attempt_id)
        .where(Attempt.user_id == user_id, Attempt.lesson_id == lesson_id)
        .order_by(Feedback.created_at.desc())
    )
    feedback = (await db.execute(stmt)).scalar_one_or_none()
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No feedback found for this lesson")
    return feedback


@router.get("/users/{user_id}/lessons/{lesson_id}/summary", response_model=LessonSummaryResponse)
async def get_lesson_summary(user_id: int, lesson_id: int, db: AsyncSession = Depends(get_db)):
    """Tổng kết kết quả luyện tập của bài học."""
    stmt = select(UserLessonProgress).where(
        UserLessonProgress.user_id == user_id,
        UserLessonProgress.lesson_id == lesson_id,
    )
    prog = (await db.execute(stmt)).scalar_one_or_none()
    if not prog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No progress found for this lesson")

    return {
        "lesson_id": lesson_id,
        "user_id": user_id,
        "total_attempts": prog.total_attempts,
        "correct_attempts": prog.completed_attempts,
        "average_score": prog.last_score,
        "is_completed": prog.is_completed,
        "summary_message": "Hoàn thành xuất sắc!" if prog.is_completed else "Cần cố gắng thêm.",
    }
