from pony.orm import db_session
from telegram import Update
from telegram.ext import CallbackContext

from termin_bot import model


class Appointments:
    APPOINTMENTS = [
        "Anmeldung einer Wohnung 1",
        "Anmeldung einer Wohnung 2",
    ]

    def get_commands(self) -> list:
        return [
            appointment.replace(" ", "_").lower() for appointment in self.APPOINTMENTS
        ]

    def get_commands_dict(self) -> dict:
        return {
            appointment.replace(" ", "_").lower(): appointment
            for appointment in self.APPOINTMENTS
        }


APPOINTMENTS = Appointments()


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
        type_text += f"\- `{command}` \({label}\)\n"

    list_text = f"""
Here are the available types:
{type_text}
    """

    update.message.reply_markdown_v2(list_text)


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

    # TODO: Model logic

    update.message.reply_text(f"Successfully subscribed to {appointment}")


def command_unsubscribe(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("You must provide appointment")

        return

    appointment = context.args[0]

    # TODO: Model logic

    update.message.reply_text(f"Successfully subscribed to {appointment}")


def command_subscriptions(update: Update, _context: CallbackContext):
    telegram_username = update.effective_user.username
    termins = model.find_user_appointments(telegram_username)

    subscriptions = ""
    for termin in termins:
        subscriptions += f"\- `{termin}`\n"

    termins_text = f"""
Here are all your subscriptions:

{subscriptions}
    """

    update.message.reply_markdown_v2(termins_text)


def command_uninstall(update: Update, _context: CallbackContext):
    telegram_username = update.effective_user.username

    try:
        model.delete_user(telegram_username)
    except ValueError:
        pass

    update.message.reply_markdown_v2(
        f"Successfully removed all data about `{telegram_username}`"
    )
