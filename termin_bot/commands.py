from telegram import Update
from telegram.ext import CallbackContext


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


def command_start(update: Update, _context: CallbackContext):
    user = update.effective_user

    welcome_text = fr"""
Hi {user.name},

Welcome to the Berlin Termin Bot\!

A place where you can get notified for free appointments on the Berlin Services website\.

Start by issuing `/list` to see available appointment types\.

Then subscribe with `/subscribe <appointment>`\.

To unregister use `/unregister <appointment`\.

To list your subscriptions use `/subscribed`
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
    update.message.reply_text("Coming soon...")
