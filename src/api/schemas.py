"""Esquemas Pydantic da API de classificação de saúde da plantação (Issue #3).

A entrada usa nomes em inglês (amigáveis ao cliente HTTP); o `main.py` faz o mapeamento
para os nomes PT-BR esperados pelo pipeline serializado em `src/ml/models/`.
"""

from typing import Literal

from pydantic import BaseModel, Field

# Culturas aceitas — exatamente as strings usadas no treino (OneHotEncoder).
# Qualquer outro valor é rejeitado na validação (422) em vez de gerar one-hot vazio.
CropName = Literal[
    "Cocoa, beans",
    "Oil palm fruit",
    "Rice, paddy",
    "Rubber, natural",
]


class PredictRequest(BaseModel):
    """Condições climáticas + cultura de uma observação a classificar."""

    crop: CropName = Field(..., description="Nome da cultura (exatamente como no dataset).")
    precipitation: float = Field(..., description="Precipitação (mm/dia).")
    specific_humidity: float = Field(..., description="Umidade específica a 2 m (g/kg).")
    relative_humidity: float = Field(..., description="Umidade relativa a 2 m (%).")
    temperature: float = Field(..., description="Temperatura a 2 m (°C).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "crop": "Cocoa, beans",
                "precipitation": 2248.92,
                "specific_humidity": 17.72,
                "relative_humidity": 83.4,
                "temperature": 26.01,
            }
        }
    }


class PredictResponse(BaseModel):
    """Resultado da classificação de saúde."""

    health: Literal["Saudável", "Não Saudável"] = Field(
        ..., description="Rótulo de saúde relativo à mediana da cultura."
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Probabilidade associada à classe predita."
    )

    model_config = {
        "json_schema_extra": {"example": {"health": "Saudável", "confidence": 0.82}}
    }


class HealthResponse(BaseModel):
    """Status do serviço."""

    status: Literal["ok"] = "ok"
    model_loaded: bool