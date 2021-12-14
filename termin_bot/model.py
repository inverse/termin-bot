from math import ceil
from typing import Dict, List, Optional

from pony.orm import Database, PrimaryKey, Required, Set, select

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
        raise MaxTerminException(MAX_TERMINS)

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


def fetch_appointments() -> List[Dict[str, str]]:
    return [{a.name: a.label} for a in Appointment.select()]


def _find_appointment(appointment: str) -> Appointment:
    return Appointment.get(name=appointment)


def _find_user(telegram_id: int) -> Optional[User]:
    user = User.get(telegram_id=telegram_id)
    return user


class Appointments:
    DEFAULT_PAGE_SIZE = 10

    def __init__(self, data: List[Dict[str, str]]):
        self._data = data
        self._appointments = [k for d in data for k in d]
        self.total: int = len(data)

    def get_appointment_names(self) -> list:
        return self._appointments

    def get_paginated_appointments(
        self, page: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> List[Dict[str, str]]:
        start = page * page_size
        end = start + page_size

        return self._data[start:end]

    def get_total_page_sizes(self, page_size: int = DEFAULT_PAGE_SIZE) -> int:
        return ceil(self.total / page_size)
