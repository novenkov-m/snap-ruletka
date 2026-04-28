from fastapi import FastAPI
from .api import auth, photos
from .database import engine
from .models.models import Base

app = FastAPI(title="snap ruletka")

# Регистрация роутеров
app.include_router(auth.router)
app.include_router(photos.router)

@app.on_event("startup")
async def startup():
    # Создание таблиц (только для разработки, для прода используй alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "PhotoSwap API is running"}