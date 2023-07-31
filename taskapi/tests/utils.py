from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Task


async def generate_user(
        session: AsyncSession,
        raw_password: str | None = None
) -> tuple[User, str]:
    """
    Generate User and save it to testing database.
    Returns tuple of (User, raw_password).
    """
    # Generate user data
    username = str(uuid4())
    email = f"{username}@email.com"
    raw_password_to_set = raw_password if raw_password else str(uuid4())

    user = User(
        email=email,
    )
    user.set_password(raw_password_to_set)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user, raw_password


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
