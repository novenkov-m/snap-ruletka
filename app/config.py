from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_region: str = "us-east-1"
    s3_use_ssl: bool = False

    max_upload_size_mb: int = 10
    photo_max_pixels: int = 1920
    thumbnail_max_pixels: int = 300

    class Config:
        env_file = ".env"

settings = Settings()