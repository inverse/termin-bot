import logging
from os.path import abspath

from environs import Env

from termin_bot.model import setup_database


def get_env() -> Env:
    env = Env()
    env.read_env()
    return env


def is_debug() -> bool:
    env = get_env()
    return env.bool("DEBUG", False)


def bootstrap():
    log_level = logging.DEBUG if is_debug() else logging.INFO
    logging.basicConfig(level=log_level)

    logging.getLogger("urllib3").setLevel(logging.WARNING)

    env = get_env()
    setup_database(abspath(env("DB_PATH")))
