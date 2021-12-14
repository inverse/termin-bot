class TerminBotException(Exception):
    pass


class MaxTerminException(TerminBotException):
    max_value: int

    def __init__(self, max_value: int):
        self.max_value = max_value
