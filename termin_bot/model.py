from typing import Dict, List, Optional

from pony.orm import Database, PrimaryKey, Required, Set, db_session, select

from termin_bot.exceptions import MaxTerminException
from termin_bot.scraper import ScrapedAppointment

MAX_TERMINS = 3


db = Database()


class User(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    telegram_id = Required(int, unique=True)
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


def find_users_for_appointment(appointment_identifier: int) -> list[User]:
    query = select(
        u
        for u in User  # type: ignore
        for t in u.termins
        if t.appointment.identifier == appointment_identifier
    )

    return query.fetch()


def find_user_subscriptions(telegram_id: int) -> List[Appointment]:
    user = _find_user(telegram_id)

    if not user:
        return []

    return [t.appointment for t in user.termins]


def add_user_appointment(telegram_id: int, appointment_identifier: str):
    user = _find_user(telegram_id)
    if not user:
        user = User(telegram_id=telegram_id)

    if len(user.termins) >= MAX_TERMINS:
        raise MaxTerminException(
            f"{user.telegram_id} already has {len(user.termins)}/{MAX_TERMINS} termins"
        )

    appointment = _find_appointment(appointment_identifier)
    Termin(appointment=appointment, user=user)


def remove_user_appointment(telegram_id: int, appointment_identifier: str):
    user = _find_user(telegram_id)
    if not user:
        return

    for termin in user.termins:
        if appointment_identifier == termin.appointment.name:
            termin.delete()


def delete_user(telegram_id: int):
    try:
        user = User.get(telegram_id=telegram_id)
        user.delete()
    except ValueError:
        pass


def find_user(telegram_id: int) -> Optional[User]:
    return _find_user(telegram_id)


def find_appointments() -> List[int]:
    return [t.appointment.identifier for t in Termin.select()]


def update_appointments(appointments: List[ScrapedAppointment]):
    for appointment in appointments:
        Appointment(
            name=appointment.name,
            label=appointment.label,
            identifier=appointment.identifier,
        )
        db.commit()


def fetch_appointments() -> Dict[str, str]:
    return {a.name: a.label for a in Appointment.select()}


def _find_appointment(appointment: str) -> Appointment:
    return Appointment.get(name=appointment)


def _find_user(telegram_id: int) -> Optional[User]:
    user = User.get(telegram_id=telegram_id)
    return user
