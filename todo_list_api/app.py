from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todo_list_api.routers import auth, todos, users
from todo_list_api.schemas.root import HealthCheckResponse

app = FastAPI(title='ToDo List API')
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=HealthCheckResponse)
async def read_root():
    return {'message': 'Hello World!'}


@app.get(
    '/api/v1/hello-world',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
async def read_hello_world():
    return '<html><body><h1>Hello World!</h1></body></html>'
