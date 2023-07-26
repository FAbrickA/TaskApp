from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Task
from db.session import get_session

from .config import API_PREFIX
from .schemas import Task as TaskSchema, TasksList, AddNewTask, UpdateTask
from ..auth.utils import get_current_user

router = APIRouter(prefix=API_PREFIX)


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        task_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user.id).limit(1)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find the task",
        )

    task_response = TaskSchema.model_validate(task, from_attributes=True)
    return task_response


@router.get("/", response_model=TasksList)
async def get_all_tasks(
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    await session.refresh(user, attribute_names=["tasks"])
    tasks = user.tasks
    tasks_list_schema = TasksList.model_validate(tasks)
    return tasks_list_schema


@router.post("/", status_code=status.HTTP_200_OK)
async def add_new_task(
        task_schema: AddNewTask,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    task = Task(**task_schema.model_dump())
    task.user_id = user.id
    session.add(task)
    await session.commit()


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
        task_id: int,
        task_schema: UpdateTask,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user.id).limit(1)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find the task",
        )

    data_to_update = task_schema.model_dump(exclude_unset=True)
    for attr, value in data_to_update.items():
        setattr(task, attr, value)

    session.add(task)
    await session.commit()


@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user.id).limit(1)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find the task",
        )

    await session.delete(task)
    await session.commit()
