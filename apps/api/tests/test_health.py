def test_health_check_returns_response_envelope(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    assert body["meta"] == {}
    assert body["data"]["status"] == "ok"
    assert body["data"]["service"] == "FinRoute API"
    assert body["data"]["database_configured"] is True
