from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero_course.app import app


def test_root_should_return_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_api_v1_should_return_html_hello_world():
    client = TestClient(app)

    response = client.get('/api/v1/hello-world')

    assert response.text == '<html><body><h1>Hello World!</h1></body></html>'
    assert response.status_code == HTTPStatus.OK
