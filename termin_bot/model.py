from pony.orm import Database, PrimaryKey, Required, Set, db_session

db = Database()


class User(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    telegram_username = Required(str, unique=True)
    termins = Set("Termin")


class Termin(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    appointment = Required(str)


def setup_database(location: str):
    db.bind(provider="sqlite", filename=location, create_db=True)
    db.generate_mapping(create_tables=True)


@db_session
def find_users_for_appointment(appointment: str) -> list[str]:
    users = User.select(lambda u: appointment in u.termins.type)

    return [u.telegram_username for u in users]


@db_session
def find_user_appointments(telegram_username: str) -> list[str]:
    user = find_user(telegram_username)

    return [t.appointment for t in user.termins]


@db_session
def remove_user_appointment(telegram_username: str, appointment: str):
    user = find_user(telegram_username)
    for termin in user.termins:
        if appointment == termin.appointment:
            termin.delete()


@db_session
def delete_user(telegram_username: str):
    try:
        user = User.get(telegram_username=telegram_username)
        user.delete()
    except ValueError:
        pass


@db_session
def find_user(telegram_username: str) -> User:
    return _find_user(telegram_username)


def _find_user(telegram_username: str) -> User:
    user = User.get(telegram_username=telegram_username)

    if not user:
        raise ValueError(f"No user found with username {telegram_username}")

    return user
