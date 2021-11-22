from datetime import datetime
from typing import List

from termin_bot import model, scraper
from termin_bot.scraper import AppointmentResult


def handle_appointments(appointments: List[int]):
    results = scraper.fetch_available_appointments(appointments)
    for result in results:
        process_appointment_result(result)


def process_appointment_result(result: AppointmentResult):
    users = model.find_users_for_appointment(result.appointment_identifier)
    for user in users:
        notify_user(user.telegram_id, result.dates)


def notify_user(user: str, dates: List[datetime]):
    pass
