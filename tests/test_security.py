from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from jwt import decode, encode

from todo_list_api.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)

EXPIRE = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)


def test_create_jwt():
    claims = {'test': 'test'}
    token = create_access_token(claims)
    decoded = decode(token, SECRET_KEY, ALGORITHM)

    assert decoded['test'] == claims['test']
    assert 'exp' in decoded


def test_jwt_invalid(client):
    response = client.delete(
        '/api/v1/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_claims_without_sub(client, user):
    invalid_token = encode(
        {
            'sub': '',
            'exp': EXPIRE,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {invalid_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_email_doesnt_exists(client, user):
    token = encode(
        {
            'sub': 'invalid@email.com',
            'exp': EXPIRE,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User doesnt exists'}
