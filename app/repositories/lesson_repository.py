from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.lesson import Lesson
from app.models.lesson_item import LessonItem
from app.models.user_lesson_progress import UserLessonProgress


class LessonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_lessons_by_version(self, version_id: int, user_id: Optional[int] = None) -> List[tuple]:
        # Lấy danh sách bài học kèm progress của user (nếu có user_id)
        stmt = (
            select(Lesson, UserLessonProgress)
            .outerjoin(
                UserLessonProgress,
                (UserLessonProgress.lesson_id == Lesson.id) & (UserLessonProgress.user_id == user_id)
            )
            .where(Lesson.version_id == version_id, Lesson.is_active == True)
            .order_by(Lesson.order_index)
        )
        result = await self.db.execute(stmt)
        return result.all()

    async def get_lesson_by_id(self, lesson_id: int) -> Optional[Lesson]:
        stmt = (
            select(Lesson)
            .options(selectinload(Lesson.lesson_items))
            .where(Lesson.id == lesson_id, Lesson.is_active == True)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_lesson_item_by_id(self, item_id: int) -> Optional[LessonItem]:
        stmt = select(LessonItem).where(LessonItem.id == item_id, LessonItem.is_active == True)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def count_lesson_items(self, lesson_id: int) -> tuple[int, int]:
        # Trả về (tổng số items, số items active)
        total_stmt = select(func.count(LessonItem.id)).where(LessonItem.lesson_id == lesson_id)
        active_stmt = select(func.count(LessonItem.id)).where(LessonItem.lesson_id == lesson_id, LessonItem.is_active == True)
        
        total = await self.db.scalar(total_stmt) or 0
        active = await self.db.scalar(active_stmt) or 0
        return total, active
    async def create_lesson_with_items(self, version_id: int, data) -> Lesson:
        """Tạo bài học mới cùng lesson_items (POST /versions/{vid}/lessons)."""
        from app.schemas.lesson import LessonCreateRequest  # local import tránh vòng

        assert isinstance(data, LessonCreateRequest)
        lesson = Lesson(
            version_id=version_id,
            title=data.title,
            description=data.description,
            order_index=data.order_index,
            is_active=data.is_active,
        )
        self.db.add(lesson)
        await self.db.flush()

        for i in data.items:
            item = LessonItem(
                lesson_id=lesson.id,
                sign_label=i.sign_label,
                item_type=i.item_type,
                difficulty=_difficulty_to_int(i.difficulty),
                media=i.media.model_dump() if i.media else {},
                steps=[s.model_dump() for s in i.steps],
                reference_data=i.reference_data or {},
                order_index=i.order_index,
                is_active=True,
            )
            self.db.add(item)

        await self.db.commit()
        await self.db.refresh(lesson)
        return lesson


def _difficulty_to_int(difficulty: Optional[str]) -> Optional[int]:
    if difficulty is None:
        return None
    if isinstance(difficulty, int):
        return difficulty
    mapping = {"easy": 1, "medium": 2, "hard": 3, "de": 1, "vua": 2, "kho": 3}
    try:
        return int(difficulty)
    except (TypeError, ValueError):
        return mapping.get(difficulty.lower())
