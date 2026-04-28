import bcrypt

def hash_password(password: str) -> str:
    # Преобразуем пароль в байты и обрезаем до 72 байт (ограничение bcrypt)
    password_bytes = password.encode('utf-8')[:72]
    # Генерируем соль и хешируем
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    # без изменений, ваш старый код JWT
    from datetime import datetime, timedelta
    from jose import jwt
    from ..config import settings

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str):
    # без изменений
    from jose import JWTError, jwt
    from ..config import settings
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None