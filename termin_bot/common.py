import logging
from os.path import abspath

from environs import Env

from termin_bot.model import setup_database


def get_env() -> Env:
    env = Env()
    env.read_env()
    return env


def bootstrap():
    logging.basicConfig(level=logging.INFO)

    env = get_env()
    setup_database(abspath(env("DB_PATH")))
