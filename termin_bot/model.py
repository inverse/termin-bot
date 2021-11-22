from typing import Dict, List

from pony.orm import Database, PrimaryKey, Required, Set, db_session, select

from termin_bot.scraper import ScrapedAppointment

db = Database()


class User(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    telegram_username = Required(str, unique=True)
    termins = Set("Termin")


class Appointment(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    label = Required(str)
    identifier = Required(int, unique=True)
    users = Set("Termin")


class Termin(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    appointment = Required(Appointment)


def setup_database(location: str):
    db.bind(provider="sqlite", filename=location, create_db=True)
    db.generate_mapping(create_tables=True)


@db_session
def find_users_for_appointment(appointment_identifier: int) -> list[User]:
    query = select(
        u
        for u in User  # type: ignore
        for t in u.termins
        if t.appointment.identifier == appointment_identifier
    )

    return query.fetch()


@db_session
def find_user_appointments(telegram_username: str) -> List[str]:
    user = find_user(telegram_username)

    return [t.appointment.name for t in user.termins]


@db_session
def remove_user_appointment(telegram_username: str, appointment: str):
    user = find_user(telegram_username)
    for termin in user.termins:
        if appointment == termin.appointment.name:
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


@db_session
def find_appointments() -> List[int]:
    return [t.appointment.identifier for t in Termin.select()]


@db_session
def update_appointments(appointments: List[ScrapedAppointment]):
    for appointment in appointments:
        Appointment(
            name=appointment.name,
            label=appointment.label,
            identifier=appointment.identifier,
        )
        db.commit()


@db_session
def fetch_appointments() -> Dict[str, str]:
    return {a.name: a.label for a in Appointment.select()}


def _find_user(telegram_username: str) -> User:
    user = User.get(telegram_username=telegram_username)

    if not user:
        raise ValueError(f"No user found with username {telegram_username}")

    return user
