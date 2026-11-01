from typing import List, Optional
from pydantic import BaseModel


class LessonProgressResponse(BaseModel):
    lesson_id: int
    is_completed: bool
    best_score: Optional[float] = None


class VersionProgressResponse(BaseModel):
    user_id: int
    version_id: int
    total_lessons: int
    completed_lessons: int
    completion_percentage: float
    lessons: List[LessonProgressResponse]


class OverallProgressResponse(BaseModel):
    user_id: int
    completed_lessons: int
    average_score: float


class SingleLessonProgressResponse(BaseModel):
    user_id: int
    lesson_id: int
    is_completed: bool
    completed_attempts: int
    total_attempts: int
    best_score: Optional[float] = None
    last_score: Optional[float] = None