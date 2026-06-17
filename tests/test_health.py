"""
Pruebas automatizadas para el endpoint /health.
"""
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    """
    Verifica que la API se encuentre operativa.
    """

    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["estado"] == "ok"