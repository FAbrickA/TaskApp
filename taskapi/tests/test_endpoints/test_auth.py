async def test_ping(client):
    response = await client.get("api/v1/ping")
    assert response.status_code == 200
    data = response.text
    assert data.lower() == "pong"


async def test_test_db(client):
    response = await client.get("api/v1/test_db")
    print(response.text)
    assert response.status_code == 200