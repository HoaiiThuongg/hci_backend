from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# --- Progress Schemas ---
class UserProgressResponse(BaseModel):
    user_id: int
    total_lessons: int
    completed_lessons: int
    total_attempts: int
    overall_score_avg: Optional[Decimal] = None


class LessonProgressDetailResponse(BaseModel):
    lesson_id: int
    completed_attempts: int
    total_attempts: int
    best_score: Optional[Decimal] = None
    last_score: Optional[Decimal] = None
    is_completed: bool
    completed_at: Optional[datetime] = None


# --- Attempt & Feedback Schemas ---
class AttemptErrorItem(BaseModel):
    type: str = Field(..., description="handshape | orientation | location | movement")
    severity: Optional[str] = None
    details: Optional[str] = None


class AttemptCreate(BaseModel):
    user_id: int
    lesson_id: int
    lesson_item_id: int
    status: str
    is_correct: Optional[bool] = None
    predicted_sign: Optional[str] = None
    model_confidence: Optional[Decimal] = None
    score: Optional[Decimal] = None
    duration_ms: Optional[int] = None
    feedback_mode: str = "adaptive"
    # FE (phương án B) gửi kèm để BE lưu log — dùng cho thống kê + error-history
    errors: List[AttemptErrorItem] = []
    client_feedback_level: Optional[int] = None
    landmarks_data: Optional[dict] = None


class AttemptResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    lesson_item_id: int
    status: str
    is_correct: Optional[bool] = None
    predicted_sign: Optional[str] = None
    model_confidence: Optional[Decimal] = None
    score: Optional[Decimal] = None
    duration_ms: Optional[int] = None
    feedback_mode: str
    feedback_level_shown: Optional[int] = None
    is_completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackResponse(BaseModel):
    id: int
    attempt_id: int
    mode: str
    level: Optional[int] = None
    target_error_type: Optional[str] = None
    message: Optional[str] = None
    suggested_action: Optional[str] = None
    media: Dict[str, Any] = {}


class LessonSummaryResponse(BaseModel):
    lesson_id: int
    user_id: int
    total_attempts: int
    correct_attempts: int
    average_score: Optional[Decimal] = None
    is_completed: bool
    summary_message: str


# --- Settings Schemas ---
class FeedbackModeUpdate(BaseModel):
    mode: str = Field(..., description="fixed | adaptive")


# --- Collector Schemas ---
class CollectorSampleCreate(BaseModel):
    lesson_item_id: int
    user_id: Optional[int] = None
    label: str
    # FE gửi mảng frame [[[x,y,z]×21] × frames]; dict cũng chấp nhận (tương thích cũ)
    landmarks: Any
    metadata: Optional[dict] = {}


class CollectorBatchCreate(BaseModel):
    samples: List[CollectorSampleCreate]
