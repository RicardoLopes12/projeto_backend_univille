import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal

@pytest.fixture
def client():
    # Banco em memória
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)
