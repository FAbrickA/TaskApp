from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Task


async def generate_user(session: AsyncSession, raw_password: str | None = None) -> User:
    """
    Generate User and save it to testing database.
    Returns User
    """

    # Generate user data
    username = str(uuid4())
    email = f"{username}@email.com"
    raw_password = raw_password if raw_password else str(uuid4())

    user = User(
        email=email,
    )
    user.set_password(raw_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


def generate_task() -> Task:
    """
    Generate Task without saving it to testing database.
    Returns Task
    """
    task = Task(
        title=f"title_{str(uuid4())}",
        description=f"description_{str(uuid4())}",
        is_done=False,
    )
    return task
