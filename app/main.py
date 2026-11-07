from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend for adaptive sign language learning",
    version="1.1.0",
)

# CORS — FE chạy ở localhost:5173/3000 phải gọi được
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error envelope thống nhất: {error_code, message, details}
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/")
def root():
    return {
        "message": "Welcome to Signora API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)
