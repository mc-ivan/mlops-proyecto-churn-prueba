# API Predictiva de Churn con FastAPI

Proyecto desarrollado como parte del módulo de ML-Ops y Puesta en Producción.

## Descripción

Esta aplicación implementa un modelo de Machine Learning para estimar el riesgo de abandono (churn) de clientes utilizando FastAPI como capa de servicio.

El modelo fue entrenado utilizando datos sintéticos y posteriormente serializado mediante Joblib para su consumo desde una API REST.

## Variables de entrada

- antiguedad
- cargo_mensual
- reclamos

## Endpoints disponibles

### GET /

Verifica que el servicio esté activo.

### GET /health

Valida que la API y el modelo se encuentren disponibles.

### POST /predict

Genera una predicción de riesgo de abandono.

Ejemplo:

```json
{
  "antiguedad": 12,
  "cargo_mensual": 95.5,
  "reclamos": 3
}
```

### GET /model-metadata

Devuelve información del modelo entrenado:

- versión
- métricas
- variables utilizadas
- versión de scikit-learn

## Ejecución

Instalar dependencias:

```
pip install -r requirements.txt
```

Entrenar modelo:

```
python src/entrenar_modelo.py
```

Ejecutar API:

```
python -m uvicorn api.main:app --reload
```

## Autor
Ivan Mamani Condori