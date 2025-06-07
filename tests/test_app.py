from http import HTTPStatus

from todo_list_api.schemas import UserPublic


def test_root_get_should_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_api_v1_get_should_return_html_hello_world(client):
    response = client.get('/api/v1/hello-world')

    assert response.text == '<html><body><h1>Hello World!</h1></body></html>'
    assert response.status_code == HTTPStatus.OK


def test_api_v1_users_post_should_create_user(client):
    response = client.post(
        '/api/v1/users',
        json={
            'username': 'test_name',
            'email': 'email@example.com',
            'password': 'test123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test_name',
        'email': 'email@example.com',
    }


def test_api_v1_users_get_should_return_empty_users(client):
    response = client.get('/api/v1/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_api_v1_users_get_should_return_one_in_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/api/v1/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_api_v1_users_put_should_update_user(client, user):
    response = client.put(
        '/api/v1/users/1',
        json={
            'username': 'name_updated',
            'email': 'newemail@example.com',
            'password': 'uPd4t$d',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'name_updated',
        'email': 'newemail@example.com',
    }


def test_api_v1_users_put_should_raise_exception(client):
    response = client.put(
        '/api/v1/users/-1',
        json={
            'username': 'name_updated',
            'email': 'newemail@example.com',
            'password': 'uPd4t$d',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.put(
        '/api/v1/users/2',
        json={
            'username': 'name_updated',
            'email': 'newemail@example.com',
            'password': 'uPd4t$d',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_v1_users_get_should_return_user(client, user):
    response = client.get('/api/v1/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'email@example.com',
    }


def test_api_v1_users_get_should_raise_exception(client):
    response = client.get('/api/v1/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get('/api/v1/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_api_v1_users_delete_should_remove_user(client, user):
    response = client.delete('/api/v1/users/1')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


def test_api_v1_users_delete_should_raise_exception(client):
    response = client.delete('/api/v1/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.delete('/api/v1/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
