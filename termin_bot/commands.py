from telegram import ForceReply, Update
from telegram.ext import CallbackContext


class Commands:
    START = "start"
    HELP = "help"


def command_start(update: Update, _context: CallbackContext):
    user = update.effective_user

    welcome_text = fr"""
Hi {user.name}\!

Welcome to the Berlin Termin Bot\.

A place where you can get notified for free appointments on the Berlin Services website\.
    """

    update.message.reply_markdown_v2(welcome_text)


def command_help(update: Update, _context: CallbackContext):
    update.message.reply_text("Help coming soon....")
