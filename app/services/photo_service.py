import uuid
from io import BytesIO
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import UploadFile, HTTPException, status
from ..models.models import Photo, View, User, PhotoStatus
from ..config import settings
from ..schemas.schemas import PhotoOut, LikeResponse
from .storage import upload_file, generate_presigned_url
from ..utils.security import decode_access_token

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

async def process_and_upload(file: UploadFile, user_id: uuid.UUID) -> Photo:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Только JPEG, PNG или WebP")

    contents = await file.read()
    # Проверка размера
    if len(contents) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Файл больше {settings.max_upload_size_mb}MB")

    img = Image.open(BytesIO(contents)).convert("RGB")
    # Очистка EXIF – сохраняем без метаданных
    output = BytesIO()
    img.save(output, format="JPEG", quality=85)
    output.seek(0)

    # Ресайз, если больше лимита
    if max(img.size) > settings.photo_max_pixels:
        img.thumbnail((settings.photo_max_pixels, settings.photo_max_pixels), Image.LANCZOS)
        output = BytesIO()
        img.save(output, format="JPEG", quality=85)
        output.seek(0)

    # Создание миниатюры
    thumb = img.copy()
    thumb.thumbnail((settings.thumbnail_max_pixels, settings.thumbnail_max_pixels), Image.LANCZOS)
    thumb_output = BytesIO()
    thumb.save(thumb_output, format="JPEG", quality=80)
    thumb_output.seek(0)

    # Генерация ключей
    ext = "jpg"
    base_key = f"{user_id}/{uuid.uuid4()}.{ext}"
    thumb_key = f"{user_id}/thumb_{uuid.uuid4()}.{ext}"

    # Загрузка в S3
    upload_file(output.read(), base_key, "image/jpeg")
    upload_file(thumb_output.read(), thumb_key, "image/jpeg")

    # Запись в БД (синхронно, но вызываем из асинхронного контекста)
    return base_key, thumb_key

async def upload_photo(db: AsyncSession, user: User, file: UploadFile) -> Photo:
    base_key, thumb_key = await process_and_upload(file, user.id)
    photo = Photo(
        user_id=user.id,
        storage_key=base_key,
        thumbnail_key=thumb_key,
        status=PhotoStatus.APPROVED
    )
    db.add(photo)
    # +5 просмотров за загрузку
    user.view_balance += 5
    await db.commit()
    await db.refresh(photo)
    return photo

async def get_random_photo(db: AsyncSession, user: User) -> PhotoOut:
    if user.view_balance <= 0:
        raise HTTPException(status_code=402, detail="Нет доступных просмотров. Загрузите фото.")

    # Подзапрос ID уже просмотренных фото
    viewed_sub = select(View.photo_id).where(View.viewer_user_id == user.id)

    # Выбор случайного чужого фото в статусе APPROVED, которое ещё не просмотрено
    stmt = (
        select(Photo)
        .where(
            and_(
                Photo.user_id != user.id,
                Photo.status == PhotoStatus.APPROVED,
                Photo.id.notin_(viewed_sub)
            )
        )
        .order_by(func.random())
        .limit(1)
    )
    result = await db.execute(stmt)
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Нет новых фото для показа")

    # Запись просмотра
    view = View(viewer_user_id=user.id, photo_id=photo.id)
    db.add(view)
    user.view_balance -= 1
    await db.commit()

    # Генерация подписанных URL
    photo_url = generate_presigned_url(photo.storage_key)
    thumb_url = generate_presigned_url(photo.thumbnail_key)

    return PhotoOut(
        id=photo.id,
        url=photo_url,
        thumbnail_url=thumb_url,
        liked_by_me=False  # только что просмотрено – лайка ещё нет
    )

async def like_photo(db: AsyncSession, user: User, photo_id: uuid.UUID) -> LikeResponse:
    # Проверяем, что фото существует и не принадлежит пользователю
    photo = await db.get(Photo, photo_id)
    if not photo or photo.user_id == user.id:
        raise HTTPException(status_code=404, detail="Фото не найдено")

    # Ищем существующую запись просмотра
    view_stmt = select(View).where(
        and_(View.viewer_user_id == user.id, View.photo_id == photo_id)
    )
    result = await db.execute(view_stmt)
    view = result.scalar_one_or_none()

    if view:
        view.liked = not view.liked  # переключение лайка
    else:
        view = View(viewer_user_id=user.id, photo_id=photo_id, liked=True)
        db.add(view)
    await db.commit()
    return LikeResponse(liked=view.liked)

async def report_photo(db: AsyncSession, user: User, photo_id: uuid.UUID, reason: str = None):
    photo = await db.get(Photo, photo_id)
    if not photo or photo.user_id == user.id:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    # Меняем статус на REPORTED (можно добавить отдельную таблицу report, пока так)
    photo.status = PhotoStatus.REPORTED
    # Здесь же можно создать запись Report, если нужно
    report = Report(reporter_user_id=user.id, photo_id=photo_id, reason=reason)
    db.add(report)
    await db.commit()
    return {"detail": "Жалоба отправлена"}