from sqlalchemy import select

from backend.models import User


def test_create_user(session):
    first_name = 'Augusto'
    last_name = 'Junior'
    full_name = first_name + ' ' + last_name
    email = first_name.lower() + '@email.com'
    password = '<PASSWORD>'

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        full_name=full_name,
        email=email,
        password=password,
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.first_name == 'Augusto'))

    assert user.first_name == 'Augusto'
