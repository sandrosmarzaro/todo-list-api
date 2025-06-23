from jwt import decode

from todo_list_api.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_jwt():
    claims = {'test': 'test'}
    token = create_access_token(claims)
    decoded = decode(token, SECRET_KEY, ALGORITHM)

    assert decoded['test'] == claims['test']
    assert 'exp' in decoded
