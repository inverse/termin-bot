from pony.orm import Database, PrimaryKey, Required, Set

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    telegram_username = Required(str)
    termins = Set('Termin')


class Termin(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    type = Required(str)


def setup_database(location: str):
    db.bind(provider="sqlite", filename=location, create_db=True)
    db.generate_mapping(create_tables=True)
