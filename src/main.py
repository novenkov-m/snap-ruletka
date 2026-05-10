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

# @app.get("/")
# async def root():
#     return {"message": "Snap Ruletka API is running"}

from fastapi.middleware.cors import CORSMiddleware

# Разрешить все origins (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # или конкретный порт, типа "http://localhost:5500"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#------------------
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# app = FastAPI(title="SnapRuletka MVP")

# Монтируем папку static, чтобы файлы были доступны по /static/...
app.mount("/static", StaticFiles(directory="static"), name="static")

# По запросу "/" отдаём index.html
# @app.get("/")
# async def root():
#     return FileResponse(os.path.join("static", "index.html"))
@app.get("/")
async def root():
    return FileResponse("templates/index.html")

@app.get("/app.html")
async def app_page():
    return FileResponse("templates/app.html")