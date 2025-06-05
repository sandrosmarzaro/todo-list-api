from dataclasses import asdict

from sqlalchemy import select

from todo_list_api.models import User


def test_should_create_user_in_db(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test_name', email='test@email.com', password='test123'
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.id == 1))

        assert user.username == 'test_name'
        assert user.email == 'test@email.com'
        assert user.password == 'test123'
        assert asdict(user) == {
            'id': 1,
            'username': 'test_name',
            'email': 'test@email.com',
            'password': 'test123',
            'created_at': time,
            'updated_at': time,
        }
