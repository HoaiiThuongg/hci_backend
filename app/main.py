from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend for adaptive sign language learning",
    version="1.0.0",
)


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