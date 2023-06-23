import sqlalchemy as sa

from .base_model import BaseModel

from db.utils import generate_password_hash, check_password_hash


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    email = sa.Column(sa.VARCHAR(255), nullable=False)

    # actual length of hash will be 64, using sha256
    # length = 128 was made to prevent migrations if hashing algorythm is changed
    password_hash = sa.Column(sa.VARCHAR(128), nullable=False)

    def set_password(self, password):
        """ Set new password_hash by password """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Check if password is correct """
        return check_password_hash(password, self.password_hash)
