import boto3
from botocore.config import Config
from ..config import settings
from urllib.parse import urljoin

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.s3_endpoint,
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region,
    use_ssl=settings.s3_use_ssl,
    config=Config(signature_version="s3v4"),
)

def generate_presigned_url(key: str, expiration: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket, "Key": key},
        ExpiresIn=expiration,
    )

def upload_file(file_data: bytes, key: str, content_type: str = "image/jpeg"):
    s3_client.put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=file_data,
        ContentType=content_type,
    )