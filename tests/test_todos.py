from http import HTTPStatus

import pytest

from .conftest import TodoFactory


def test_v1_post_create_todo(client, token):
    response = client.post(
        '/api/v1/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'task',
            'description': 'test',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'task',
        'description': 'test',
        'state': 'draft',
    }


@pytest.mark.asyncio
async def test_v1_get_read_many_todos(session, client, token, user):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(expected_todos, user_id=user.id))
    await session.commit()

    response = client.get(
        '/api/v1/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_v1_get_read_with_pagination(session, client, token, user):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/api/v1/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_v1_get_read_with_title_filter(session, client, token, user):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, title='test 1'
        )
    )
    session.add_all(TodoFactory.create_batch(expected_todos, user_id=user.id))
    await session.commit()

    response = client.get(
        '/api/v1/todos/?title=test 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_v1_get_read_with_description_filter(
    session, client, token, user
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description='description'
        )
    )
    session.add_all(TodoFactory.create_batch(expected_todos, user_id=user.id))
    await session.commit()

    response = client.get(
        '/api/v1/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_v1_get_read_with_state_filter(session, client, token, user):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(expected_todos, user_id=user.id, state='todo')
    )
    session.add_all(
        TodoFactory.create_batch(expected_todos, user_id=user.id, state='done')
    )
    await session.commit()

    response = client.get(
        '/api/v1/todos/?state=todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_v1_delete_todo(session, client, token, user):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    response = client.delete(
        f'/api/v1/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


@pytest.mark.asyncio
async def test_v1_delete_todo_raise_error(session, client, token, user):
    response = client.delete(
        '/api/v1/todos/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task dont exists'}
