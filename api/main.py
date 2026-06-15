from pathlib import Path

import joblib
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "modelo_churn_v1.joblib"

VERSION_MODELO = "modelo_churn_v1"
AUTOR = "Ivan Mamani"

METADATA_PATH = (
    PROJECT_ROOT
    / "models"
    / "modelo_churn_v1_metadata.json"
)

if not MODEL_PATH.exists():
    raise RuntimeError(
        "No se encontró el modelo serializado. "
        "Ejecute primero: python src\\entrenar_modelo.py"
    )

modelo = joblib.load(MODEL_PATH)

class ClienteEntrada(BaseModel):
    antiguedad: int = Field(
        ...,
        ge=0,
        le=120,
        description="Antigüedad del cliente en meses",
        examples=[12],
    )

    cargo_mensual: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Cargo mensual",
        examples=[95.5],
    )

    reclamos: int = Field(
        ...,
        ge=0,
        le=50,
        description="Cantidad de reclamos",
        examples=[3],
    )

class PrediccionSalida(BaseModel):

    prediccion: str
    probabilidad: float
    version_modelo: str
    autor: str

app = FastAPI(
    title="API de predicción de churn",
    description="Servicio ML-Ops para estimar riesgo de abandono",
    version="1.0.0",
)


@app.get("/")
def inicio():

    return {
        "mensaje": "Servicio ML-Ops activo",
        "estado": "ok",
        "autor": AUTOR,
        "estudiante": "Ivan Mamani Condori"
    }

@app.get("/health")
def health():
    return {
        "estado": "ok",
        "modelo": VERSION_MODELO,
    }

@app.get("/info")
def info():
    return {
        "modelo": VERSION_MODELO,
        "autor": AUTOR,
        "variables": [
            "antiguedad",
            "cargo_mensual",
            "reclamos"
        ],
        "descripcion": "Modelo de prediccion de abandono de clientes"
    }

@app.get("/model-metadata")
def model_metadata():
    try:
        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as archivo:
            metadata = json.load(archivo)
        return metadata

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible leer los metadatos del modelo."
        ) from exc

@app.post("/predict", response_model=PrediccionSalida)
def predict(datos: ClienteEntrada):
    try:
        X = [[
            datos.antiguedad,
            datos.cargo_mensual,
            datos.reclamos,
        ]]

        probabilidad = float(
            modelo.predict_proba(X)[0][1]
        )

        etiqueta = (
            "alto_riesgo"
            if probabilidad >= 0.50
            else "bajo_riesgo"
        )

        return PrediccionSalida(
            prediccion=etiqueta,
            probabilidad=round(probabilidad, 4),
            version_modelo=VERSION_MODELO,
            autor=AUTOR,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="No fue posible generar la predicción."
        ) from exc