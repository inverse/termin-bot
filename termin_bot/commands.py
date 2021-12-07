from typing import Dict

from telegram import Update
from telegram.ext import CallbackContext

from termin_bot import model


class Appointments:
    def __init__(self, data: Dict[str, str]):
        self.data = data

    def get_commands(self) -> list:
        return list(self.data.keys())

    def get_commands_dict(self) -> dict:
        return self.data


APPOINTMENTS = Appointments(model.fetch_appointments())


class Commands:
    START = "start"
    LIST = "list"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    SUBSCRIPTIONS = "subscriptions"
    UNINSTALL = "uninstall"


def command_start(update: Update, _context: CallbackContext):
    user = update.effective_user

    welcome_text = fr"""
Hi {user.name},

Welcome to the Berlin Termin Bot\!

A place where you can get notified for free appointments on the Berlin Services website\.

Available commands:
\- `/list` \- see available appointment
\- `/subscribe` \- subscribe to appointment
\- `/unsubscribe` \- unsubscribe from an appointment
\- `/subscribed` \- view your subscriptions
\- `/uninstall` \- remove all saved state
    """

    update.message.reply_markdown_v2(welcome_text)


def command_list(update: Update, _context: CallbackContext):
    type_text = ""
    for command, label in APPOINTMENTS.get_commands_dict().items():
        type_text += f"- `{command}` ({label})\n"

    list_text = f"""
Here are the available types:
{type_text}
    """
    update.message.reply_markdown_v2(_format_text(list_text))


def command_subscribe(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("You must provide appointment")

        return

    appointment = context.args[0]

    if appointment not in APPOINTMENTS.get_commands():
        update.message.reply_text(
            f"{appointment} not in list of available appointments"
        )

        return

    telegram_id = update.effective_user.id
    model.add_user_appointment(telegram_id, appointment)

    update.message.reply_text(f"Successfully subscribed to {appointment}")


def command_unsubscribe(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("You must provide appointment")

        return

    appointment = context.args[0]

    telegram_id = update.effective_user.id
    model.remove_user_appointment(telegram_id, appointment)

    update.message.reply_text(f"Successfully subscribed to {appointment}")


def command_subscriptions(update: Update, _context: CallbackContext):
    telegram_id = update.effective_user.id
    termins = model.find_user_appointments(telegram_id)

    subscriptions = ""
    for termin in termins:
        subscriptions += f"- `{termin}`\n"

    termins_text = f"""
Here are all your subscriptions:

{subscriptions}
    """

    update.message.reply_markdown_v2(_format_text(termins_text))


def command_uninstall(update: Update, _context: CallbackContext):
    telegram_id = update.effective_user.id

    try:
        model.delete_user(telegram_id)
    except ValueError:
        pass

    update.message.reply_markdown_v2(f"Successfully removed all data about you")


def _format_text(text: str) -> str:
    text = text.replace("-", "\-")
    text = text.replace("(", "\(")
    text = text.replace(")", "\)")
    text = text.replace(".", "\.")
    return text
