from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todo_list_api.schemas import MessageClass

app = FastAPI(title='ToDo List API')


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageClass)
def read_root():
    return {'message': 'Hello World!'}


@app.get(
    '/api/v1/hello-world',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def read_hello_world():
    return '<html><body><h1>Hello World!</h1></body></html>'
