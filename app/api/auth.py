from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.schemas import UserRegister, Token, UserOut
from ..services.auth_service import register, login, get_current_user
from ..models.models import User

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/register", response_model=UserOut)
async def register_endpoint(data: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await register(db, data)
    return user

@router.post("/token", response_model=Token)
async def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await login(db, form_data.username, form_data.password)

async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Неавторизован")
    return user

#--------------------------
@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user