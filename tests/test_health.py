async def test_health(client):
    """`GET /health` returns 200 and a healthy status."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
