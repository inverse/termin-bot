import logging
from typing import List

from telegram.ext import ExtBot

from termin_bot import common, model, scraper
from termin_bot.message import get_notification_message
from termin_bot.scraper import AppointmentResult

logger = logging.getLogger(__name__)


def handle_appointments(appointments: List[int]):
    results = scraper.fetch_available_appointments(appointments)
    for result in results:
        process_appointment_result(result)


def process_appointment_result(result: AppointmentResult):
    users = model.find_users_for_appointment(result.appointment_identifier)
    for user in users:
        notify_user(user.telegram_id, result)


def notify_user(telegram_id: int, result: AppointmentResult):
    env = common.get_env()
    bot = ExtBot(token=env("BOT_TOKEN"))
    bot.send_message(chat_id=telegram_id, text=get_notification_message(result))
