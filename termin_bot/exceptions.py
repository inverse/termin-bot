class TerminBotException(Exception):
    pass


class NoUserException(TerminBotException):
    pass


class MaxTerminException(TerminBotException):
    pass
