class NotJsonError(Exception):
    pass


class NoData(Exception):
    pass


class ConfirmationLinkError(Exception):
    def __init__(self, text_exception):
        self.text = text_exception


class RegisterUserError(Exception):
    def __init__(self, text_exception):
        self.text = text_exception
