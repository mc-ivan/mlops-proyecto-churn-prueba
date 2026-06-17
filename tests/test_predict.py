"""
Pruebas automatizadas para el endpoint /predict.
"""
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_predict():
    """
    Verifica una predicción válida.
    """

    payload = {
        "antiguedad": 24,
        "cargo_mensual": 80.0,
        "reclamos": 1,
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert "prediccion" in body
    assert "probabilidad" in body
