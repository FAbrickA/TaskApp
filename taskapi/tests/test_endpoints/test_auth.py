from fastapi import status

from api.v1.endpoints.auth.schemas import UserData, Token
from api.v1.endpoints.auth.utils import decode_token
from db.models import User


class TestAuthToken:
    url = "/api/v1/auth/token"

    async def test_get_token(self, client, user, raw_password):
        # make request to get token
        user_data = UserData(
            email=user.email,
            password=raw_password,
        )
        response = await client.post(self.url, json=user_data.model_dump())
        assert response.status_code == status.HTTP_200_OK

        # extract token and check its type
        data = response.json()
        token = Token(**data)
        assert token.token_type.lower() == "bearer"

        # check access token
        payload = decode_token(token.access_token)
        assert "email" in payload
        assert payload.get("email") == user.email
