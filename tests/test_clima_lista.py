from tabela import Clima
from database import SessionLocal

def test_listar_climas(client):
    db = SessionLocal()
    db.add(Clima(descricao="Joinville 25°"))
    db.add(Clima(descricao="Curitiba 18°"))
    db.commit()
    db.close()

    resp = client.get("/climas")

    assert resp.status_code == 200
    lista = resp.json()
    assert len(lista) >= 2
