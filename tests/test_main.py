# tests/test_main.py

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database import get_db, Base
from app.config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="module")
def client():
    # Set up the database for testing
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Tear down the database
    Base.metadata.drop_all(bind=engine)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

def test_create_configuration(client):
    response = client.post(
        "/create_configuration",
        json={"country_code": "IN", "requirements": {"BusinessName": "string", "PAN": "string", "GSTIN": "string"}}
    )
    assert response.status_code == 200
    assert response.json()["country_code"] == "IN"

def test_get_configuration(client):
    response = client.get("/get_configuration/IN")
    assert response.status_code == 200
    assert response.json()["country_code"] == "IN"

def test_update_configuration(client):
    response = client.post(
        "/update_configuration",
        json={"country_code": "IN", "requirements": {"BusinessName": "string", "PAN": "string", "GSTIN": "string", "ExtraField": "string"}}
    )
    assert response.status_code == 200
    assert "ExtraField" in response.json()["requirements"]

def test_delete_configuration(client):
    response = client.delete("/delete_configuration/IN")
    assert response.status_code == 200
    assert response.json() == {"detail": "Configuration deleted"}

    response = client.get("/get_configuration/IN")
    assert response.status_code == 404
