from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class MediaSchema(BaseModel):
    demo_video: Optional[str] = None
    ref_image: Optional[str] = None
    anim_slow: Optional[str] = None


class StepSchema(BaseModel):
    step_number: int
    instruction: str


class LessonItemCreateRequest(BaseModel):
    sign_label: str
    item_type: str
    difficulty: Optional[str] = None
    order_index: int
    media: Optional[MediaSchema] = None
    steps: List[StepSchema] = []
    reference_data: Optional[dict] = None


class LessonCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int
    difficulty: Optional[str] = None
    is_active: bool = True
    items: List[LessonItemCreateRequest]


class LessonItemResponse(BaseModel):
    id: int
    lesson_id: int
    sign_label: str
    item_type: str
    difficulty: Optional[int] = None
    description: Optional[str] = None
    media: Dict[str, Any]
    steps: List[Any]
    order_index: int
    is_active: bool

    class Config:
        from_attributes = True


class LessonResponse(BaseModel):
    id: int
    version_id: int
    title: str
    description: Optional[str] = None
    order_index: int
    is_active: bool
    # Có thể bổ sung trạng thái hoàn thành của user nếu cần
    is_completed: Optional[bool] = False 
    completed_attempts: Optional[int] = 0

    class Config:
        from_attributes = True


class LessonDetailResponse(LessonResponse):
    lesson_items: List[LessonItemResponse] = []


class FeedbackConfigResponse(BaseModel):
    lesson_id: int
    default_mode: str  # fixed | adaptive
    levels_available: List[int]
    settings: Dict[str, Any]


class LessonAvailabilityResponse(BaseModel):
    lesson_id: int
    is_available: bool
    total_items: int
    active_items: int
    message: str