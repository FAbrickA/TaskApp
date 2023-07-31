import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"

    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    title = sa.Column(sa.VARCHAR(100), nullable=False)
    description = sa.Column(sa.VARCHAR(2000))
    is_done = sa.Column(sa.BOOLEAN, default=False, nullable=False)

    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())

    user_id = sa.Column(sa.INTEGER, sa.ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="tasks")
