"""API FastAPI de classificação de saúde da plantação — Entrega "Ir Além" (Issue #3).

Carrega o pipeline serializado `src/ml/models/health_classifier.pkl` (produzido pelo
notebook da Issue #1) e expõe:

- `GET  /health`  -> status do serviço
- `POST /predict` -> {"health": "Saudável" | "Não Saudável", "confidence": float}

O `.pkl` É o pipeline sklearn completo (ColumnTransformer + RandomForestClassifier), logo
o pré-processamento aqui é **idêntico** ao do treino: basta alimentar um DataFrame com os
nomes de coluna PT-BR esperados pelo `ColumnTransformer`. Não reconstruímos o preprocessor
para evitar qualquer inconsistência/leakage.

Como rodar (a partir da raiz do repo):

    pip install -r requirements.txt
    python -m uvicorn src.api.main:app --reload --port 8000

Depois abra http://localhost:8000/docs para a UI interativa (Swagger).
"""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

import joblib
import pandas as pd
from fastapi import FastAPI

from src.api.schemas import HealthResponse, PredictRequest, PredictResponse

# --- Caminhos (robustos ao diretório de execução) ----------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]          # .../fase-5-pbl-agro
MODELS_DIR = REPO_ROOT / "src" / "ml" / "models"
CLASSIFIER_PATH = MODELS_DIR / "health_classifier.pkl"
LABEL_MAP_PATH = MODELS_DIR / "label_map.json"

# Estado global preenchido no lifespan (evita recarregar o modelo a cada request).
state: dict = {"pipeline": None, "label_map": None}


def _load_label_map() -> dict:
    with open(LABEL_MAP_PATH, encoding="utf-8") as f:
        return json.load(f)


# Mapeamento: nomes amigáveis (esquema) -> nomes PT-BR esperados pelo ColumnTransformer.
# Derivado do label_map para não duplicar strings manualmente.
def _column_map(label_map: dict) -> dict:
    num = label_map["numeric_features"]
    cat = label_map["categorical_feature"]
    return {
        "crop": cat,
        "precipitation": num[0],
        "specific_humidity": num[1],
        "relative_humidity": num[2],
        "temperature": num[3],
    }


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Carrega pipeline + metadados uma única vez na subida do serviço.
    state["pipeline"] = joblib.load(CLASSIFIER_PATH)
    state["label_map"] = _load_label_map()
    yield
    state["pipeline"] = None
    state["label_map"] = None


app = FastAPI(
    title="FarmTech Solutions — Classificador de Saúde da Plantação",
    description=(
        "API do desafio 'Ir Além'. Consome o classificador de saúde serializado na "
        "Issue #1 e classifica uma observação (cultura + condições climáticas) como "
        "Saudável ou Não Saudável."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Verifica se o serviço está no ar e o modelo carregado."""
    return HealthResponse(model_loaded=state["pipeline"] is not None)


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    """Classifica a saúde de uma observação climática + cultura.

    O rótulo é **relativo à mediana** da cultura (lógica derivada no notebook): uma
    observação com Rendimento >= mediana da sua cultura seria 'Saudável'. Aqui o
    classificador aproxima essa decisão apenas a partir das condições climáticas.
    """
    pipeline = state["pipeline"]
    if pipeline is None:  # pragma: no cover - protegido pelo lifespan
        raise RuntimeError("Modelo não carregado.")

    col_map = _column_map(state["label_map"])

    # Monta um DataFrame de 1 linha com os nomes PT-BR esperados pelo ColumnTransformer.
    row = pd.DataFrame([{
        col_map["crop"]: req.crop,
        col_map["precipitation"]: req.precipitation,
        col_map["specific_humidity"]: req.specific_humidity,
        col_map["relative_humidity"]: req.relative_humidity,
        col_map["temperature"]: req.temperature,
    }])

    pred = int(pipeline.predict(row)[0])
    proba = pipeline.predict_proba(row)[0]
    confidence = float(max(proba))

    health_label = "Saudável" if pred == 1 else "Não Saudável"
    return PredictResponse(health=health_label, confidence=confidence)