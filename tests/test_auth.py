from http import HTTPStatus

from freezegun import freeze_time


def test_api_v1_token_create_token(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_api_v1_token_raise_exception_when_invalid_email(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={
            'username': 'invalid@email.com',
            'password': user.clean_password,
        },
    )

    response.status_code == HTTPStatus.UNAUTHORIZED
    response.json() == {'detail': 'Email doesnt exists!'}


def test_api_v1_token_raise_exception_when_invalid_password(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': 'invalid_password'},
    )

    response.status_code == HTTPStatus.UNAUTHORIZED
    response.json() == {'detail': 'Incorrect password!'}


def test_token_expired_after_time(client, user):
    with freeze_time('2025-06-26 18:00:00'):
        response = client.post(
            '/api/v1/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-06-26 18:31:00'):
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
