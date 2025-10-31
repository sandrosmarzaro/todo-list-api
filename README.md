# ToDo List API
A RESTful async API for managing a ToDo list, built with FastAPI and PostgreSQL, featuring JWT authentication, database migrations, and comprehensive testing. It's make in [FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/) course by [Dunossauro](https://dunossauro.com/).


## Tech Stack

- [Python 3.13](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [PyTest](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Poetry](https://python-poetry.org/)
- [Ruff](https://docs.astral.sh/ruff/)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sandrosmarzaro/todo-list-api.git
cd todo-list-api/
```

### 2. Configure environment variables

Create a `.env` file at the project root with the database credentials and keys expected by `compose.yml`:

```env
DATABASE_URL='postgres://user:password@localhost:5432/mydatabase'
SECRET_KEY='abcde12345'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Feel free to use any values—just keep them in sync with your environment.

### 3. Build and start the containers

```bash
docker compose build        # one-time image build
docker compose up -d        # start app & database in the background
```

The API will be reachable at http://localhost:8000 when the containers are healthy.

### 4. Apply database migrations

```bash
docker compose exec app alembic upgrade head
```

### 5. Run the tests

```bash
docker compose exec app task test
```

### 6. API documentation

The project ships with interactive, auto-generated OpenAPI documentation available at the following endpoints:

| Endpoint | Description |
|----------|-------------|
| `/docs`  | Swagger UI |
| `/redoc` | ReDoc |

These routes are served as soon as the application container is running.

### 7. Key API endpoints

Base path: `/api/v1`

**Users**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/users/` | List users / create user |
| GET/PUT/PATCH/DELETE | `/users/<id>/` | User detail & management |


**Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/token` | User login to obtain JWT token |
| POST | `/auth/refresh_token` | Refresh JWT token |


**Todos**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/todos/` | List todos / create todo |
| GET/PUT/PATCH/DELETE | `/todos/<id>/` | Todo detail & management |


All endpoints require authentication unless explicitly noted otherwise (e.g., user creation and login).

---

To stop everything:

```bash
docker compose down
```
