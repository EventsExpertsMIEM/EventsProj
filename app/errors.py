from .rest_api import *
from .exceptions import *
from .util import send_500_email
from sqlalchemy.exc import IntegrityError


def add_error_handlers(app):
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, no_access)
    app.register_error_handler(404, route_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(415, wrong_request_type)
    app.register_error_handler(500, send_500_email)

    app.register_error_handler(IntegrityError, make_400)
    app.register_error_handler(KeyError, make_400)
    app.register_error_handler(AttributeError, make_400)
    app.register_error_handler(WrongIdError, make_404)
    app.register_error_handler(RegisterUserError, make_409)
    app.register_error_handler(ConfirmationLinkError, make_409)
    app.register_error_handler(JoinUserError, make_409)
    app.register_error_handler(NotJsonError, make_415)
    app.register_error_handler(WrongDataError, make_422)
    app.register_error_handler(ValueError, make_422)
    app.register_error_handler(IndexError, make_422)


def on_json_loading_failed(err, e):
    raise NotJsonError('Wrong json!')
