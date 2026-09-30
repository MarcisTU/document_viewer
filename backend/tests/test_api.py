from fastapi.testclient import TestClient

from app import app


# Use fastapi TestClient to be able to test API endpoints directly (without parallel running instance.)
client = TestClient(app)


def test_get_documents_rejects_invalid_limit():
    response = client.get("/api/v1/documents?limit=0")

    assert response.status_code == 422


def test_get_documents_rejects_limit_above_maximum():
    response = client.get("/api/v1/documents?limit=501")

    assert response.status_code == 422


def test_get_documents_rejects_negative_offset():
    response = client.get("/api/v1/documents?offset=-1")

    assert response.status_code == 422
