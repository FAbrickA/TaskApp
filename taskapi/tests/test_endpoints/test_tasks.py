from fastapi import status

from api.v1.endpoints.tasks.schemas import AddNewTask, Task as TaskSchema, TasksList, UpdateTask, Task

from .utils import (
    add_task_to_database,
    get_not_existing_task_id,
    is_task_exist,
    add_tasks_to_database,
)

URL_BASE = "/api/v1/tasks/"


class TestGetTask:
    """
    Test GET /api/v1/tasks/{task_id}
    Get one task of current user by task.id
    Authenticated user only.
    """

    @staticmethod
    def get_url(task_id) -> str:
        return f"{URL_BASE}{task_id}"

    async def test_get_task(self, task, auth_client):
        """
        Test successful getting task.
        """
        initial_task_schema = TaskSchema.model_validate(task, from_attributes=True)

        response = await auth_client.get(self.get_url(task.id))
        assert response.status_code == status.HTTP_200_OK

        # Extract task data from response
        data = response.json()
        task_response_data = TaskSchema(**data)

        assert initial_task_schema == task_response_data

    async def test_get_task_not_exist(self, session, auth_client):
        """
        Test getting task that not exist
        """
        unknown_task_id = await get_not_existing_task_id(session)

        response = await auth_client.get(self.get_url(unknown_task_id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_task_another_user(self, session, auth_client, user_factory, task_factory):
        """
        Test getting task that you have no access to because it belongs to another user.
        """
        another_user = await user_factory()
        task = task_factory()  # task of another user
        await add_task_to_database(session, task, another_user.id)

        response = await auth_client.get(self.get_url(task.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_task_not_authenticated(self, client, task):
        """
        Test getting task that you have no access to because you are not authorized.
        """
        response = await client.get(self.get_url(task.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetTasks:
    """
    Test GET /api/v1/tasks/
    Get all tasks of current user.
    Authenticated user only.
    """

    NUMBER_OF_TASKS = 3

    @staticmethod
    def get_url() -> str:
        return URL_BASE

    async def test_get_all_tasks(self, session, user, auth_client, task_factory):
        """
        Test successful getting all user's tasks.
        """
        tasks = [task_factory() for _ in range(self.NUMBER_OF_TASKS)]
        await add_tasks_to_database(session, tasks, user_id=user.id)

        initial_task_schemas = [
            TaskSchema.model_validate(task, from_attributes=True) for task in tasks]

        response = await auth_client.get(self.get_url())
        assert response.status_code == status.HTTP_200_OK

        # Extract tasks data from response
        data = response.json()
        tasks_response_data = TasksList.model_validate(data).root
        assert len(tasks_response_data) == self.NUMBER_OF_TASKS

        # Prepare data
        tasks_sorting_func = lambda task: task.id
        initial_task_schemas.sort(key=tasks_sorting_func)
        tasks_response_data.sort(key=tasks_sorting_func)

        # Compare
        for t1, t2 in zip(initial_task_schemas, tasks_response_data):
            assert t1 == t2

    async def test_get_all_tasks_empty(self, session, user, auth_client):
        """
        Test successful getting all user's tasks when user has no tasks.
        """
        # Check no user's tasks presented
        await session.refresh(user, attribute_names=['tasks'])
        assert len(user.tasks) == 0

        response = await auth_client.get(self.get_url())
        assert response.status_code == status.HTTP_200_OK

        # Check still no tasks presented
        data = response.json()
        tasks_response_data = TasksList.model_validate(data).root
        assert len(tasks_response_data) == 0

    async def test_get_all_tasks_not_authenticated(self, client):
        """
        Test getting tasks when you are not authorized.
        """
        response = await client.get(self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAddTask:
    """
    Test POST /api/v1/tasks/
    Add new task of current user.
    Authenticated user only.
    """

    @staticmethod
    def get_url() -> str:
        return URL_BASE

    @staticmethod
    def make_task_request_data(task: Task) -> AddNewTask:
        return AddNewTask(
            title=task.title,
            description=task.description,
            is_done=task.is_done,
        )

    async def test_add_task(self, session, auth_client, task_factory):
        """
        Test successful adding task.
        """
        task = task_factory()

        # Check task not exist
        assert not await is_task_exist(session, task)

        # Make post request to add the task
        task_request_data = self.make_task_request_data(task)
        response = await auth_client.post(self.get_url(), json=task_request_data.model_dump())
        assert response.status_code == status.HTTP_200_OK

        # Check task exist after request
        assert await is_task_exist(session, task)

    async def test_add_task_not_authenticated(self, client, task_factory):
        """
        Test adding task when user is not authenticated
        """
        task = task_factory()

        # Make post request to add the task
        task_request_data = self.make_task_request_data(task)
        response = await client.post(self.get_url(), json=task_request_data.model_dump())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTaskUpdate:
    """
    Test PUT /api/v1/tasks/{task_id}
    Update task's data of current user.
    Authenticated user only.
    """

    @staticmethod
    def get_url(task_id):
        return f"{URL_BASE}{task_id}"

    @staticmethod
    def make_task_request_data(task: Task, all_fields: bool = True) -> UpdateTask:
        if all_fields:
            return UpdateTask(
                title=f"{task.title}_new",
                description=f"{task.description}_new",
                is_done=not task.is_done,
            )
        return UpdateTask(
            title=f"{task.title}_new",
        )

    async def test_update_task_all_fields(self, session, task, auth_client):
        """
        Test successful update of all task's fields
        """
        # Update task data
        new_task_data = self.make_task_request_data(task, all_fields=True)
        response = await auth_client.put(
            self.get_url(task.id),
            json=new_task_data.model_dump(exclude_unset=True)
        )
        assert response.status_code == status.HTTP_200_OK

        # Check changes
        await session.refresh(task)
        assert task.title == new_task_data.title
        assert task.description == new_task_data.description
        assert task.is_done == new_task_data.is_done

    async def test_update_task_one_field(self, session, task, auth_client):
        """
        Test successful update of only one task's field
        """
        # Update task data
        new_task_data = self.make_task_request_data(task, all_fields=False)
        response = await auth_client.put(
            self.get_url(task.id),
            json=new_task_data.model_dump(exclude_unset=True)
        )
        assert response.status_code == status.HTTP_200_OK

        # Check changes
        await session.refresh(task)
        assert task.title == new_task_data.title

    async def test_update_task_no_data(self, session, task, auth_client):
        """
        Test update task when no data passed
        """
        response = await auth_client.put(
            self.get_url(task.id),
            json={}  # no data passed
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_update_task_another_user(self, session, auth_client, user_factory, task_factory):
        """
        Test update task when you have no access to it because it belongs to another user
        """
        another_user = await user_factory()
        task = task_factory()  # another_user's task
        await add_task_to_database(session, task, user_id=another_user.id)

        # Save old task data before update
        task_schema = TaskSchema.model_validate(task, from_attributes=True)

        # Try to update task that belongs to another user
        new_task_data = self.make_task_request_data(task, all_fields=True)
        response = await auth_client.put(
            self.get_url(task.id),
            json=new_task_data.model_dump(exclude_unset=True)
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Check changes have not been applied
        await session.refresh(task)
        assert task.title == task_schema.title
        assert task.description == task_schema.description
        assert task.is_done == task_schema.is_done

    async def test_update_task_not_exist(self, session, auth_client, task_factory):
        """
        Test updating task that not exist
        """
        task = task_factory()

        unknown_task_id = await get_not_existing_task_id(session)

        new_task_data = self.make_task_request_data(task, all_fields=True)
        response = await auth_client.put(
            self.get_url(unknown_task_id),
            json=new_task_data.model_dump(exclude_unset=True)
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_task_not_authenticated(self, session, task, client):
        """
        Test updating task when user is not authenticated
        """
        # Save old task data before update
        task_schema = TaskSchema.model_validate(task, from_attributes=True)

        new_task_data = self.make_task_request_data(task, all_fields=True)
        response = await client.put(
            self.get_url(task.id),
            json=new_task_data.model_dump(exclude_unset=True)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check changes have not applied
        await session.refresh(task)
        assert task.title == task_schema.title
        assert task.description == task_schema.description
        assert task.is_done == task_schema.is_done


class TestDeleteTask:
    """
    Test DELETE /api/v1/tasks/{task_id}
    Update task's data of current user.
    Authenticated user only.
    """

    @staticmethod
    def get_url(task_id: int):
        return f"{URL_BASE}{task_id}"

    async def test_delete_task(self, session, task, auth_client, task_factory):
        """
        Test successful deleting task
        """
        response = await auth_client.delete(self.get_url(task.id))
        assert response.status_code == status.HTTP_200_OK

        # Check task have been deleted
        assert not await is_task_exist(session, task)

    async def test_delete_task_not_exist(self, session, auth_client):
        """
        Test deleting task when task is not exist
        """
        unknown_task_id = await get_not_existing_task_id(session)

        response = await auth_client.delete(self.get_url(unknown_task_id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_task_another_user(self, session, user, auth_client, user_factory, task_factory):
        """
        Test deleting task when it belongs to another user
        """
        another_user = await user_factory()
        task = task_factory()  # another_user's task
        await add_task_to_database(session, task, user_id=another_user.id)

        # Try to delete another_user's task
        response = await auth_client.delete(self.get_url(task.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Check task still exists
        assert await is_task_exist(session, task)

    async def test_delete_task_not_authenticated(self, session, task, client):
        """
        Test deleting task when user is not authenticated
        """
        response = await client.delete(self.get_url(task.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check task still exists
        assert await is_task_exist(session, task)
