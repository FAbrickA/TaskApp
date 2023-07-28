from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Task, User


async def is_task_exist(session: AsyncSession, task: Task) -> bool:
    """
    Check if Task exist by task.title
    """
    stmt = select(Task.id).where(Task.title == task.title).limit(1)
    result = await session.execute(stmt)
    return bool(result.fetchone())


async def get_not_existing_task_id(session: AsyncSession) -> int:
    """
    Get Task.id that is not presented in database.
    May not be the most efficient solution, but for test purposes it is quite OK.
    """
    async def _is_task_id_exists():
        stmt = select(Task.id).where(Task.id == task_id).limit(1)
        result = await session.scalar(stmt)
        is_task_id_exist = bool(result)
        return is_task_id_exist

    task_id = 100
    while await _is_task_id_exists():
        task_id += 1

    return task_id


async def add_tasks_to_database(
        session: AsyncSession,
        tasks: list[Task],
        user_id: int | None = None
) -> None:
    """
    Add Tasks to database and refresh them.
    You must define either task.user_id or user_id.
    """

    for task in tasks:
        if task.user_id is None:
            if user_id is None:
                raise ValueError("Task must have user_id attribute")
            task.user_id = user_id

        session.add(task)
        await session.commit()
        await session.refresh(task)


async def add_task_to_database(
        session: AsyncSession,
        task: Task,
        user_id: int | None = None,
) -> None:
    """
    Function-sugar for adding a single Task to database.
    """

    return await add_tasks_to_database(session, [task], user_id=user_id)


async def is_user_exist(session: AsyncSession, user: User) -> bool:
    """
    Check if User exists by User.email
    """
    stmt = select(User.id).where(User.email == user.email).limit(1)
    result = await session.execute(stmt)
    return bool(result.fetchone())
