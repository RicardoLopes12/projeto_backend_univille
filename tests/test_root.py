def test_root_redirect_or_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
