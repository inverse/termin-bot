from telegram import  Update
from telegram.ext import CallbackContext


TYPES = [
    "Anmeldung einer Wohnung 1",
    "Anmeldung einer Wohnung 2",
]

class Commands:
    START = "start"
    HELP = "help"
    LIST = "list"


def command_start(update: Update, _context: CallbackContext):
    user = update.effective_user

    welcome_text = fr"""
Hi {user.name}\!

Welcome to the Berlin Termin Bot\.

A place where you can get notified for free appointments on the Berlin Services website\.\

Start by issuing `/list` to see available appointment types\.\

Then subscribe `/subscribe <type>`\.
    """

    update.message.reply_markdown_v2(welcome_text)


def command_help(update: Update, _context: CallbackContext):
    update.message.reply_text("Help coming soon....")

def command_list(update: Update, _context: CallbackContext):

    type_text = ""
    for type in TYPES:
        type_text += f"\- `{type}`\n"

    list_text = f"""
Here are the available types:
{type_text}
    """

    update.message.reply_markdown_v2(list_text)
