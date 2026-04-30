from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.photo_service import upload_photo, get_random_photo, like_photo, report_photo
from ..schemas.schemas import PhotoOut, LikeResponse
from ..api.auth import get_current_active_user
from ..models.models import User

router = APIRouter(prefix="/photos", tags=["photos"])

@router.post("/upload", response_model=dict)
async def upload(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    photo = await upload_photo(db, current_user, file)
    return {"id": str(photo.id), "status": photo.status}

@router.get("/random", response_model=PhotoOut)
async def random_photo(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await get_random_photo(db, current_user)

@router.post("/{photo_id}/like", response_model=LikeResponse)
async def like(
    photo_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await like_photo(db, current_user, photo_id)

@router.post("/{photo_id}/report")
async def report(
    photo_id: str,
    reason: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await report_photo(db, current_user, photo_id, reason)