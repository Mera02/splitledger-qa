import httpx
import pytest


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def api_client():
    with httpx.Client(
        base_url=BASE_URL,
        timeout=5.0,
    ) as client:
        yield client