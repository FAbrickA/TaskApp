from fastapi import status

from api.v1.endpoints.auth.schemas import UserData, Token
from api.v1.endpoints.auth.utils import decode_token
from db.models import User

URL_BASE = "/api/v1/auth/"


class TestToken:
    @staticmethod
    def get_url() -> str:
        return f"{URL_BASE}token"

    async def test_get_token(self, client, user, raw_password):
        """
        Test successful getting token
        """
        user_data = UserData(
            email=user.email,
            password=raw_password,
        )

        response = await client.post(self.get_url(), json=user_data.model_dump())
        assert response.status_code == status.HTTP_200_OK

        # Extract token and check its type
        data = response.json()
        token = Token(**data)
        assert token.token_type.lower() == "bearer"

        # Check access token
        payload = decode_token(token.access_token)
        assert "email" in payload
        assert payload.get("email") == user.email

    async def test_incorrect_login(self, client, user, raw_password):
        """
        Test getting token when user's login is incorrect
        """
        incorrect_email = f"incorrect.{user.email}"

        user_data = UserData(
            email=incorrect_email,
            password=raw_password,
        )

        response = await client.post(self.get_url(), json=user_data.model_dump())
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_incorrect_password(self, client, user, raw_password):
        """
        Test getting token when user's raw_password is incorrect
        """
        incorrect_password = f"incorrect_{raw_password}"

        user_data = UserData(
            email=user.email,
            password=incorrect_password,
        )

        response = await client.post(self.get_url(), json=user_data.model_dump())
        assert response.status_code == status.HTTP_403_FORBIDDEN
