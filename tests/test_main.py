from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Correcting the token format for the OAuth2PasswordBearer scheme
headers = {"Authorization": "Bearer admin_token"}

def test_create_plan():
    response = client.post(
        "/plans/",
        json={
            "name": "Basic",
            "description": "Basic plan",
            "api_permissions": "service1",
            "usage_limit": 100
        },
        headers=headers  # Include authentication header
    )
    print("Response JSON:", response.json())  # Debug to understand validation errors
    assert response.status_code == 200
    assert response.json()["name"] == "Basic"
