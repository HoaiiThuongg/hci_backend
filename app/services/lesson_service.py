from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson import (
    LessonCreateRequest,
    LessonResponse,
    LessonDetailResponse,
    LessonItemResponse,
    FeedbackConfigResponse,
    LessonAvailabilityResponse,
)


class LessonService:
    def __init__(self, db: AsyncSession):
        self.repo = LessonRepository(db)

    async def get_version_lessons(self, version_id: int, user_id: Optional[int] = None) -> List[dict]:
        rows = await self.repo.get_lessons_by_version(version_id, user_id)
        response = []
        for lesson, progress in rows:
            lesson_data = {
                "id": lesson.id,
                "version_id": lesson.version_id,
                "title": lesson.title,
                "description": lesson.description,
                "order_index": lesson.order_index,
                "is_active": lesson.is_active,
                "is_completed": progress.is_completed if progress else False,
                "completed_attempts": progress.completed_attempts if progress else 0,
            }
            response.append(lesson_data)
        return response

    async def get_lesson_detail(self, lesson_id: int) -> LessonDetailResponse:
        lesson = await self.repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
        return lesson  # SQLAlchemy model map trực tiếp qua Pydantic nhờ from_attributes=True

    async def get_lesson_item_detail(self, item_id: int) -> LessonItemResponse:
        item = await self.repo.get_lesson_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson item not found")
        return item

    async def get_feedback_config(self, lesson_id: int) -> FeedbackConfigResponse:
        # Kiểm tra lesson có tồn tại không
        lesson = await self.repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
        
        # Logic cấu hình feedback (có thể lấy từ app_settings hoặc mặc định theo lesson)
        return FeedbackConfigResponse(
            lesson_id=lesson_id,
            default_mode="adaptive",
            levels_available=[1, 2, 3],
            settings={
                "allow_skip": True,
                "max_retries": 5,
                "show_skeleton": True
            }
        )

    async def check_lesson_availability(self, lesson_id: int) -> LessonAvailabilityResponse:
        lesson = await self.repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

        total, active = await self.repo.count_lesson_items(lesson_id)
        is_available = active > 0

        return LessonAvailabilityResponse(
            lesson_id=lesson_id,
            is_available=is_available,
            total_items=total,
            active_items=active,
            message="Lesson is ready for practice" if is_available else "Lesson has no active items available"
        )

    async def create_lesson(self, version_id: int, request: LessonCreateRequest) -> LessonDetailResponse:
        """Tạo bài học mới + items, trả về chi tiết đầy đủ."""
        from app.models.version import Version

        version = await self.repo.db.get(Version, version_id)
        if version is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")

        lesson = await self.repo.create_lesson_with_items(version_id, request)
        # Re-fetch với selectinload để serialize lesson_items (async không lazy-load được)
        return await self.get_lesson_detail(lesson.id)
