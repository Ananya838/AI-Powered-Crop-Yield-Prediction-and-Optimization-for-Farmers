def test_weather_and_soil_endpoints(client, auth_token):
    weather_response = client.get(
        "/api/v1/data/weather",
        params={"district": "Pune", "season": "kharif"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert weather_response.status_code == 200
    weather = weather_response.json()
    assert weather["district"] == "Pune"
    assert "avg_rainfall_mm" in weather

    soil_response = client.get(
        "/api/v1/data/soil",
        params={"latitude": 18.52, "longitude": 73.85},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert soil_response.status_code == 200
    soil = soil_response.json()
    assert soil["latitude"] == 18.52
    assert "nitrogen" in soil
