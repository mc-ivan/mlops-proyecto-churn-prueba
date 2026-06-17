# API Predictiva de Churn con FastAPI

Proyecto desarrollado como parte del módulo de ML-Ops y Puesta en Producción.

## Descripción

Esta aplicación implementa un modelo de Machine Learning para estimar el riesgo de abandono (churn) de clientes utilizando FastAPI como capa de servicio.

El modelo fue entrenado utilizando datos sintéticos y posteriormente serializado mediante Joblib para su consumo desde una API REST.

La solución incorpora prácticas de ML-Ops para facilitar la reproducibilidad, observabilidad y monitoreo mediante Docker, Prometheus y Grafana.

---

# Arquitectura de la Solución

```text
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Modelo ML   │
└──────┬──────┘
       │
       ├─────────────► Prometheus
       │                    │
       │                    ▼
       │                Grafana
       │
       ▼
Predicción
```

---

# Variables de Entrada

El modelo utiliza las siguientes variables:

* antiguedad
* cargo_mensual
* reclamos

---

# Artefactos Generados

Modelo serializado:

```text
models/modelo_churn_v1.joblib
```

Metadatos del modelo:

```text
models/modelo_churn_v1_metadata.json
```

---

# Endpoints Disponibles

## GET /

Verifica que el servicio esté activo.

## GET /health

Valida que la API y el modelo se encuentren disponibles.

## POST /predict

Genera una predicción de riesgo de abandono.

Ejemplo:

```json
{
  "antiguedad": 12,
  "cargo_mensual": 95.5,
  "reclamos": 3
}
```

## GET /metrics

Muestra métricas internas de la aplicación.

## GET /prometheus

Expone métricas compatibles con Prometheus.

## GET /model-metadata

Devuelve información del modelo entrenado:

* versión
* métricas
* variables utilizadas
* versión de scikit-learn

## GET /model-monitoring

Muestra indicadores operativos de la API:

* solicitudes procesadas
* errores internos
* latencia promedio
* estado operativo

## GET /model-drift

Permite visualizar indicadores básicos de riesgo de drift a partir de las anomalías detectadas durante las predicciones.

---

# Configuración mediante Variables de Entorno

Archivo:

```text
.env
```

Ejemplo:

```env
MODEL_VERSION=modelo_churn_v1
API_AUTHOR=Ivan Mamani Condori
DRIFT_THRESHOLD=10
```

---

# Ejecución Local

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Entrenar el modelo

```bash
python src/entrenar_modelo.py
```

## Ejecutar la API

```bash
python -m uvicorn api.main:app --reload
```

## Acceder a Swagger

```text
http://localhost:8000/docs
```

---

# Pruebas Automatizadas

Se implementaron pruebas automatizadas utilizando Pytest.

Archivos:

```text
tests/test_health.py
tests/test_predict.py
```

Ejecutar todas las pruebas:

```bash
python -m pytest
```

Resultado esperado:

```text
2 passed
```

---

# Ejecución con Docker

## Construir y levantar servicios

```bash
docker compose up -d --build
```

## Verificar contenedores activos

```bash
docker ps
```

## Detener servicios

```bash
docker compose down
```

## Reconstruir la solución

```bash
docker compose up -d --build
```

---

# Monitoreo

## Swagger

```text
http://localhost:8000/docs
```

## Prometheus

```text
http://localhost:9090
```

## Grafana

```text
http://localhost:3000
```

---

# Consulta de Métricas

Consultar métricas Prometheus:

```bash
curl http://localhost:8000/prometheus
```

Consultar monitoreo operativo:

```bash
curl http://localhost:8000/model-monitoring
```

Consultar riesgo de drift:

```bash
curl http://localhost:8000/model-drift
```

Consultar metadatos del modelo:

```bash
curl http://localhost:8000/model-metadata
```

---

# Logs y Diagnóstico

Ver logs de la API:

```bash
docker compose logs api
```

Seguir logs en tiempo real:

```bash
docker compose logs -f api
```

Ver logs de Prometheus:

```bash
docker compose logs prometheus
```

Ver logs de Grafana:

```bash
docker compose logs grafana
```

---

# Simulación de Tráfico

Ejecutar simulador de solicitudes:

```bash
python tests/simular_trafico.py
```

Esta utilidad permite generar tráfico artificial para observar:

* incremento de solicitudes
* métricas Prometheus
* dashboards Grafana
* comportamiento del monitoreo

---

# Monitoreo Implementado

Métricas monitoreadas:

* solicitudes HTTP totales
* predicciones realizadas
* latencia de respuesta
* códigos HTTP
* errores internos
* anomalías detectadas
* riesgo de drift

---

# Alertas Propuestas

| Evento       | Umbral         | Acción                        |
| ------------ | -------------- | ----------------------------- |
| Drift        | >10% anomalías | Revisar calidad de datos      |
| Latencia     | >500 ms        | Revisar rendimiento           |
| Errores HTTP | >5%            | Revisar logs de la aplicación |

---

# Tecnologías Utilizadas

* Python
* FastAPI
* Scikit-Learn
* Joblib
* Pydantic
* Pytest
* Docker
* Docker Compose
* Prometheus
* Grafana

---

# Autor

Ivan Mamani Condori
