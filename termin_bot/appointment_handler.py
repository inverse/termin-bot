from datetime import datetime
from typing import List

from termin_bot import model, scraper
from termin_bot.scraper import AppointmentResult


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
