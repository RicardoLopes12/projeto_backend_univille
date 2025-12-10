from unittest.mock import patch

MOCK_IP = {
    "latitude": -26.3044,
    "longitude": -48.8487,
    "city": "Joinville"
}

MOCK_OPEN_METEO = {
    "hourly": {
        "temperature_2m": [25.4]
    }
}

@patch("main.requests.get")
def test_clima_sucesso(mock_get, client):
    mock_get.side_effect = [
        type("obj", (object,), {"json": lambda: MOCK_IP}),
        type("obj", (object,), {"json": lambda: MOCK_OPEN_METEO}),
    ]

    resp = client.get("/clima")
    data = resp.json()

    assert resp.status_code == 200
    assert data["cidade"] == "Joinville"
    assert "temperatura_agora" in data


@patch("main.requests.get")
def test_clima_sem_localizacao(mock_get, client):
    mock_get.return_value.json = lambda: {"latitude": None, "longitude": None}

    resp = client.get("/clima")
    data = resp.json()

    assert "erro" in data


@patch("main.requests.get", side_effect=Exception("Falha"))
def test_clima_exception(mock_get, client):
    resp = client.get("/clima")
    data = resp.json()

    assert "erro" in data
