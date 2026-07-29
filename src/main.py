from fastapi import FastAPI
from .api import auth, photos
from .database import engine
from .models.models import Base

app = FastAPI(title="snap ruletka")

app.include_router(auth.router)
app.include_router(photos.router)

@app.on_event("startup")
async def startup():
    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from fastapi.middleware.cors import CORSMiddleware

# Разрешить все origins (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["http://localhost:5500"],
    allow_headers=["http://localhost:5500"],
)

#------------------
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("templates/index.html")
