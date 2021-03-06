from exceptions import MaxTerminException
from pony.orm import db_session
from telegram import Update
from telegram.ext import CallbackContext

from termin_bot import model

APPOINTMENTS = model.Appointments(model.fetch_appointments())


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

A place where you can get notified for free appointments on the Berlin Services website\.\

Use the `/list` command to view available appointments, then pass the appointment slug to the `/subscribe` command

Available commands:
\- `/list <page-number>` \- see available appointment - pass page-number to view a particular page
\- `/subscribe` \- subscribe to appointment
\- `/unsubscribe` \- unsubscribe from an appointment
\- `/subscriptions` \- view your subscriptions
\- `/uninstall` \- remove all saved state
    """

    update.message.reply_markdown_v2(welcome_text)


@db_session
def command_list(update: Update, context: CallbackContext):

    page = int(context.args[0] if len(context.args) > 0 else 0)
    total_pages = APPOINTMENTS.get_total_page_sizes()

    if page < 0 or page > total_pages:
        update.message.reply_text(
            f"Please provide page-number greater than 0 and less than {total_pages+1}"
        )

        return

    type_text = ""
    for appointments in APPOINTMENTS.get_paginated_appointments(page):
        for command, label in appointments.items():
            type_text += f"- `{command}` ({label})\n"

    list_text = f"""
Here are the available types:
{type_text}

Page {page}/{total_pages}
    """
    update.message.reply_markdown_v2(_format_text(list_text))


@db_session
def command_subscribe(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("You must provide appointment")

        return

    appointment = context.args[0]

    if appointment not in APPOINTMENTS.get_appointment_names():
        update.message.reply_text(
            f"{appointment} not in list of available appointments"
        )

        return

    telegram_id = update.effective_user.id
    try:
        model.add_user_appointment(telegram_id, appointment)
    except MaxTerminException as e:
        update.message.reply_text(
            f"You have already subscribed to {e.max_value} termins"
        )

        return

    update.message.reply_text(f"Successfully subscribed to {appointment}")


@db_session
def command_unsubscribe(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("You must provide appointment")

        return

    appointment = context.args[0]

    telegram_id = update.effective_user.id
    model.remove_user_appointment(telegram_id, appointment)

    update.message.reply_text(f"Successfully subscribed to {appointment}")


@db_session
def command_subscriptions(update: Update, _context: CallbackContext):
    telegram_id = update.effective_user.id
    termins = model.find_user_subscriptions(telegram_id)

    subscriptions = ""
    for termin in termins:
        subscriptions += f"- `{termin.label}` ({termin.name})\n"

    termins_text = f"""
Here are all your subscriptions:

{subscriptions}
    """

    update.message.reply_markdown_v2(_format_text(termins_text))


@db_session
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
