from http import HTTPStatus

from todo_list_api.schemas import UserPublic


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


def test_api_v1_users_post_should_raise_username_exception(client, user):
    response = client.post(
        '/api/v1/users',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists!'}


def test_api_v1_users_post_should_raise_email_exception(client, user):
    response = client.post(
        '/api/v1/users',
        json={
            'username': 'test2nd',
            'email': 'email@example.com',
            'password': 'test123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists!'}


def test_api_v1_users_get_should_return_one_in_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/api/v1/users',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_api_v1_users_put_should_update_user(client, user, token):
    response = client.put(
        '/api/v1/users/1',
        headers={'Authorization': f'Bearer {token}'},
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


def test_api_v1_users_put_should_raise_exception(client, user, token):
    response = client.put(
        '/api/v1/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'name_updated',
            'email': 'newemail@example.com',
            'password': 'uPd4t$d',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_api_v1_users_put_should_raise_exeception_when_is_not_unique(
    client, user, token
):
    client.post(
        '/api/v1/users',
        json={
            'username': 'test2nd',
            'email': 'second@email.com',
            'password': 'test123',
        },
    )
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2nd',
            'email': 'second@email.com',
            'password': 'uPd4t$d',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists!'}


def test_api_v1_users_get_should_return_user(client, user, token):
    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_api_v1_users_get_should_raise_exception(client, user, token):
    response = client.get(
        f'/api/v1/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_api_v1_users_delete_should_remove_user(client, user, token):
    response = client.delete(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


def test_api_v1_users_delete_should_raise_exception(client, user, token):
    response = client.delete(
        f'/api/v1/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
