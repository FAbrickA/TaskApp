class TestPingApp:
    url = "api/v1/health/ping_app"

    async def test_ping_app(self, client):
        response = await client.get(self.url)
        assert response.status_code == 200


class TestPingDb:
    url = "api/v1/health/ping_db"

    async def test_test_db(self, client):
        response = await client.get(self.url)
        assert response.status_code == 200
