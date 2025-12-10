import pytest
from unittest.mock import patch
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

MOCK_IP = {
    "city": "Joinville",
    "latitude": -26.3044,
    "longitude": -48.8487
}

MOCK_OPEN_METEO = {
    "hourly": {
        "temperature_2m": [25.5],
        "weather_code": [1]
    }
}

MOCK_OPENAI_RESPONSE = type("obj", (), {
    "output_text": "O clima está tão quente que derrete até pensamento."
})


@patch("main.client.responses.create")
@patch("main.requests.get")
def test_clima_ia_sucesso(mock_get, mock_ai):
    mock_get.side_effect = [
        type("obj", (object,), {"json": lambda: MOCK_IP}),
        type("obj", (object,), {"json": lambda: MOCK_OPEN_METEO}),
    ]

    mock_ai.return_value = MOCK_OPENAI_RESPONSE

    resp = client.get("/clima-ia")
    data = resp.json()

    assert resp.status_code == 200
    assert "analise_da_ia" in data
    assert isinstance(data["analise_da_ia"], str)


@patch("main.requests.get")
def test_clima_ia_sem_localizacao(mock_get):
    # latitude e longitude ausentes
    mock_get.return_value.json = lambda: {"latitude": None, "longitude": None}

    resp = client.get("/clima-ia")
    data = resp.json()

    assert resp.status_code == 200

    # Seu main SEMPRE retorna "analise_da_ia"
    assert "analise_da_ia" in data
    assert data["analise_da_ia"] == "Não foi possível obter a localização."


@patch("main.requests.get", side_effect=Exception("Falha geral"))
def test_clima_ia_exception(mock_get):
    resp = client.get("/clima-ia")
    data = resp.json()

    assert resp.status_code == 200

    # Seu main retorna sempre "analise_da_ia"
    assert "analise_da_ia" in data
    assert "Erro ao gerar análise: Falha geral" == data["analise_da_ia"]