"""
Prueba de carga básica para la API de churn.

Objetivos:
1. Generar tráfico HTTP hacia /predict.
2. Alimentar las métricas de Prometheus.
3. Visualizar actividad en Grafana.
4. Verificar estabilidad de la API.
"""

from __future__ import annotations

import random
import time

import requests

# ============================================================
# CONFIGURACIÓN
# ============================================================

# Endpoint de predicción.
API_URL = "http://localhost:8000/predict"

# Cantidad total de solicitudes a enviar.
TOTAL_SOLICITUDES = 100

# Tiempo de espera entre solicitudes (segundos).
PAUSA_MINIMA = 0.05
PAUSA_MAXIMA = 0.20


# ============================================================
# GENERACIÓN DE DATOS
# ============================================================

def generar_cliente() -> dict:
    """
    Genera datos válidos aleatorios para simular clientes.

    Los rangos utilizados son similares a los empleados
    durante el entrenamiento del modelo.
    """

    return {
        "antiguedad": random.randint(1, 120),
        "cargo_mensual": round(
            random.uniform(20, 250),
            2,
        ),
        "reclamos": random.randint(0, 10),
    }

# ============================================================
# SIMULACIÓN DE TRÁFICO
# ============================================================
def ejecutar_prueba() -> None:
    """
    Envía múltiples solicitudes hacia la API.

    Registra:
    - solicitudes exitosas
    - errores HTTP
    - excepciones de conexión
    """

    exitosas = 0
    errores = 0

    print("=" * 60)
    print("INICIANDO SIMULACIÓN DE TRÁFICO")
    print("=" * 60)

    for numero in range(1, TOTAL_SOLICITUDES + 1):
        payload = generar_cliente()

        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=10,
            )

            if response.status_code == 200:

                exitosas += 1

                print(
                    f"[{numero:03}] OK "
                    f"({response.status_code})"
                )

            else:

                errores += 1

                print(
                    f"[{numero:03}] ERROR "
                    f"({response.status_code})"
                )

        except Exception as exc:

            errores += 1

            print(
                f"[{numero:03}] EXCEPCIÓN: {exc}"
            )

        # Simula tráfico más realista.
        time.sleep(
            random.uniform(
                PAUSA_MINIMA,
                PAUSA_MAXIMA,
            )
        )

    print("\n")
    print("=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"Solicitudes exitosas : {exitosas}")
    print(f"Solicitudes con error: {errores}")
    print(f"Total enviadas       : {TOTAL_SOLICITUDES}")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    ejecutar_prueba()
    