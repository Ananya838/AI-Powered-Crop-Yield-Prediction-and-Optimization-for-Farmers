def test_register_and_login(client):
    register_payload = {
        "full_name": "Asha Farmer",
        "phone": "8888888888",
        "password": "secure123",
        "language": "hi",
    }

    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 200
    assert register_response.json()["phone"] == "8888888888"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"phone": "8888888888", "password": "secure123"},
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_yield_prediction_returns_explainability(client, auth_token):
    response = client.post(
        "/api/v1/prediction/yield",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "crop": "wheat",
            "district": "Pune",
            "village": "Hinjawadi",
            "rainfall": 640,
            "temperature": 27,
            "nitrogen": 70,
            "phosphorus": 32,
            "potassium": 28,
            "ph": 6.5,
            "irrigation": "canal",
            "season": "kharif",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["expected_yield"] > 0
    assert body["confidence_score"] > 0
    assert isinstance(body["explainability"], list)
    assert len(body["explainability"]) > 0


def test_explain_endpoint(client, auth_token):
    response = client.post(
        "/api/v1/prediction/explain",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "crop": "wheat",
            "district": "Pune",
            "village": "Hinjawadi",
            "rainfall": 640,
            "temperature": 27,
            "nitrogen": 70,
            "phosphorus": 32,
            "potassium": 28,
            "ph": 6.5,
            "irrigation": "canal",
            "season": "kharif",
        },
    )

    assert response.status_code == 200
    assert "explainability" in response.json()
