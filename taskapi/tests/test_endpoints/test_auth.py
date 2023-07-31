from uuid import uuid4

from fastapi import status

from api.v1.endpoints.auth.config import TOKEN_URL
from api.v1.endpoints.auth.schemas import UserData, Token, RegistrationData
from api.v1.endpoints.auth.utils import decode_token
from db.models import User
from tests.test_endpoints.utils import is_user_exist

URL_BASE = "/api/v1/auth"


class TestToken:
    """
    Test POST /api/v1/auth/token
    Create and get token.
    """
    @staticmethod
    def get_url() -> str:
        return f"{URL_BASE}{TOKEN_URL}"

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


class TestSignup:
    """
    Test POST /api/v1/auth/signup
    Register a new user.
    """

    @staticmethod
    def get_url() -> str:
        return f"{URL_BASE}/signup"

    @staticmethod
    def get_reg_data(user: User, raw_password: str) -> RegistrationData:
        return RegistrationData(
            email=user.email,
            password=raw_password
        )

    async def test_signup(self, session, client):
        """
        Test successful user registration
        """
        user = User(
            email=f"{str(uuid4())}@email.com",
        )
        raw_password = str(uuid4())
        user.set_password(raw_password)

        # Check user not exists
        assert not await is_user_exist(session, user)

        reg_data = self.get_reg_data(user, raw_password)
        response = await client.post(
            self.get_url(),
            json=reg_data.model_dump()
        )
        assert response.status_code == status.HTTP_200_OK

        # Check user have been appeared
        assert await is_user_exist(session, user)

    async def test_signup_email_already_registered(self, session, user, client):
        """
        Test registration when email is already registered
        """
        # Check user already exist
        assert await is_user_exist(session, user)

        reg_data = self.get_reg_data(user, "some_raw_password")
        response = await client.post(
            self.get_url(),
            json=reg_data.model_dump()
        )
        assert response.status_code == status.HTTP_409_CONFLICT
