from http import HTTPStatus


def test_root_get_should_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_api_v1_get_should_return_html_hello_world(client):
    response = client.get('/api/v1/hello-world')

    assert response.text == '<html><body><h1>Hello World!</h1></body></html>'
    assert response.status_code == HTTPStatus.OK
