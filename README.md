# TaskApp
Python FastAPI pet project to manage tasks.
Allows you to create account and when to create your tasks with
title, description, "is done" checkbox and created/updated time.

### Endpoints

Main Endpoints:  
* `GET /api/v1/tasks/{task_id}`: Get your task by id
* `PUT /api/v1/tasks/{task_id}`: Update task by id
* `DELETE /api/v1/tasks/{task_id}`: Delete task by id
* `GET /api/v1/tasks/`: Get all tasks
* `POST /api/v1/tasks/`: Add a new task

For other endpoints and schemas you can visit `/docs` url
with api documentation. 

### To run
#### Installation:
Firstly, define `.env` file. See `.env.example` for example.

Next, you need to apply database migrations.
Before it, you need to have running containers:
```
docker-compose up -d
```

Then, apply migrations:
```
docker-compose run --rm taskapi alembic upgrade head
```

#### Run application:  
```
docker-compose up -d
```

#### Stop application:
```
docker-compose stop
```

#### Run tests:
```
docker-compose run --rm taskapi pytest
```

### Technologies used
* **FastAPI** - web-framework on Python
* **PostgreSQL** as database
* **asyncpg** as database async driver
* **SQLAlchemy** - database ORM
* **docker-compose** to create and manage containers
* **PyTest** for testing 
