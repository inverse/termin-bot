from datetime import datetime
from typing import List

from scraper import AppointmentResult

from termin_bot import model, scraper


def handle_appointments(appointments: List[str]):
    results = scraper.fetch_available_appointments(appointments)
    for result in results:
        process_appointment_result(result)


def process_appointment_result(result: AppointmentResult):
    users = model.find_users_for_appointment(result.appointment)
    for user in users:
        notify_user(user, result.dates)


def notify_user(user: str, dates: List[datetime]):
    pass
