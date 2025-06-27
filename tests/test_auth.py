from http import HTTPStatus

from freezegun import freeze_time

INITIAL_TIME = '2025-06-26 18:00:00'
EXPIRED_TIME = '2025-06-26 18:31:00'


def test_api_v1_token_post_create(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_api_v1_token_post_raise_exception_when_invalid_email(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={
            'username': 'invalid@email.com',
            'password': user.clean_password,
        },
    )

    response.status_code == HTTPStatus.UNAUTHORIZED
    response.json() == {'detail': 'Email doesnt exists!'}


def test_api_v1_token_post_raise_exception_when_invalid_password(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': 'invalid_password'},
    )

    response.status_code == HTTPStatus.UNAUTHORIZED
    response.json() == {'detail': 'Incorrect password!'}


def test_api_v1_token_expired_after_time(client, user):
    with freeze_time(INITIAL_TIME):
        response = client.post(
            '/api/v1/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time(EXPIRED_TIME):
        response = client.put(
            f'/api/v1/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': user.username,
                'email': user.email,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_api_v1_refresh_token(client, token):
    response = client.post(
        '/api/v1/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_api_v1_refresh_token_after_expire_raise_exception(client, user):
    with freeze_time(INITIAL_TIME):
        response = client.post(
            '/api/v1/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time(EXPIRED_TIME):
        response = client.post(
            '/api/v1/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
