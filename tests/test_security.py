from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from jwt import decode, encode

from todo_list_api.security import create_access_token


def generate_expire(settings):
    return datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def test_create_jwt(settings):
    claims = {'test': 'test'}
    token = create_access_token(claims)
    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded['test'] == claims['test']
    assert 'exp' in decoded


def test_jwt_invalid(client):
    response = client.delete(
        '/api/v1/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_claims_without_sub(client, user, settings):
    invalid_token = encode(
        {
            'sub': '',
            'exp': generate_expire(settings),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {invalid_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_email_doesnt_exists(client, user, settings):
    token = encode(
        {
            'sub': 'invalid@email.com',
            'exp': generate_expire(settings),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User doesnt exists'}
