from fastapi import APIRouter

# Import các router từ các module endpoint tương ứng
from app.api.v1.endpoints.user import router as users_router
from app.api.v1.endpoints.version import router as versions_router
from app.api.v1.endpoints.lesson import router as lessons_router
from app.api.v1.endpoints.progress import router as progress_router
from app.api.v1.endpoints.attempt import router as attempt_router
from app.api.v1.endpoints.settings_collector import router as settings_collector_router
from app.api.v1.endpoints.history_progress import router as history_progress_router
from app.api.v1.endpoints.collector_ext import router as collector_ext_router

api_router = APIRouter()

# Đăng ký từng router vào tổng api_router
api_router.include_router(users_router)
api_router.include_router(versions_router)
api_router.include_router(lessons_router)
api_router.include_router(progress_router)
api_router.include_router(attempt_router)
api_router.include_router(settings_collector_router)
api_router.include_router(history_progress_router)
api_router.include_router(collector_ext_router)