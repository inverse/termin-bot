from pony.orm import Database, PrimaryKey, Required, Set

db = Database()


class User(db.Entity):
    id = PrimaryKey(int)
    telegram_username = Required(str, unique=True)
    termins = Set("Termin")


class Termin(db.Entity):
    id = PrimaryKey(int)
    user = Required(User)
    type = Required(str)


def setup_database(location: str):
    db.bind(provider="sqlite", filename=location, create_db=True)
    db.generate_mapping(create_tables=True)


def find_users_for_termin_type(type: str):
    users = User.select(lambda u: type in u.termins.type)

    return [u.telegram_username for u in users]


def find_user_termins(telegram_username: str) -> list[str]:
    user = User.get(telegram_username=telegram_username)

    if not user:
        raise Exception(f"No user found with username {telegram_username}")

    return [t.type for t in user.termins]
