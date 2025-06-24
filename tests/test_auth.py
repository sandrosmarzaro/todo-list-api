from http import HTTPStatus


def test_api_v1_token_create_token(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_api_v1_token_raise_exception_when_invalid_email(client):
    response = client.post(
        '/api/v1/auth/token',
        data={'username': 'invalid@email.com', 'password': 'test123'},
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
