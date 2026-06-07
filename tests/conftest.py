import pytest
from fastapi.testclient import TestClient
from src.main import app
import io
from PIL import Image

@pytest.fixture
def client():
    """Создаёт тестовый клиент для FastAPI-приложения."""
    return TestClient(app)

@pytest.fixture
def test_image():
    """Генерирует минимальное JPEG-изображение в виде байтов."""
    img = Image.new("RGB", (10, 10), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf