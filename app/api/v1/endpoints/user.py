from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)

    try:
        return await service.create_user(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[UserRead],
)
async def get_users(
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    return await service.get_users()


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    user = await service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
