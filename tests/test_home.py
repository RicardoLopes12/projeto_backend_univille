def test_home_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "<html" in resp.text.lower() or "index.html" in resp.text.lower()

def test_home_html_missing_file(client, monkeypatch):
    def mock_open(*args, **kwargs):
        raise FileNotFoundError()
    monkeypatch.setattr("builtins.open", mock_open)
    resp = client.get("/")
    assert "não encontrado" in resp.text.lower()
