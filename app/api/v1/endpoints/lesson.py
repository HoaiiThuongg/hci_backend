from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db  # Hàm dependency cung cấp AsyncSession của bạn
from app.services.lesson_service import LessonService
from app.schemas.lesson import (
    LessonResponse,
    LessonDetailResponse,
    LessonItemResponse,
    FeedbackConfigResponse,
    LessonAvailabilityResponse,
    LessonCreateRequest
)

router = APIRouter(prefix="", tags=["Lessons"])


@router.get("/lessons/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson_detail(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Lấy chi tiết một bài học và danh sách các ký hiệu (lesson items) bên trong."""
    service = LessonService(db)
    return await service.get_lesson_detail(lesson_id)


@router.get("/lesson-items/{lesson_item_id}", response_model=LessonItemResponse)
async def get_lesson_item_detail(
    lesson_item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Lấy chi tiết một ký hiệu cụ thể."""
    service = LessonService(db)
    return await service.get_lesson_item_detail(lesson_item_id)


@router.get("/lessons/{lesson_id}/feedback-config", response_model=FeedbackConfigResponse)
async def get_lesson_feedback_config(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Lấy cấu hình feedback áp dụng cho bài học."""
    service = LessonService(db)
    return await service.get_feedback_config(lesson_id)


@router.get("/lessons/{lesson_id}/availability", response_model=LessonAvailabilityResponse)
async def check_lesson_availability(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Kiểm tra nội dung bài học có khả dụng để luyện tập hay không."""
    service = LessonService(db)
    return await service.check_lesson_availability(lesson_id)

@router.post(
    "/versions/{version_id}/lessons",
    response_model=LessonDetailResponse,
    status_code=201,
    summary="Tạo bài học mới",
    description="Tạo bài học cùng danh sách ký hiệu và nội dung hướng dẫn."
)
async def create_lesson(
    version_id: int,
    request: LessonCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    service = LessonService(db)
    return await service.create_lesson(version_id, request)