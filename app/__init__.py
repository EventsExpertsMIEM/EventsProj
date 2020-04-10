from .logic.accounts import user_loader
from .config import cfg
from .rest_api import accounts, users, events, tasks, reports
from .errors import add_error_handlers, on_json_loading_failed

from flask import Flask, Request
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail
from gevent.pywsgi import WSGIServer
from gevent import monkey
from os.path import join, exists
from os import makedirs


import logging
import logging.config
import sys

for K, V in cfg.FILE_UPLOADS.FILE_SETS.items():
    path = join(cfg.FILE_UPLOADS.PARENT_FOLDER, V.FOLDER)
    if not exists(path):
        makedirs(path)
    cfg.FILE_UPLOADS.FILE_SETS[K].FOLDER = path

tmp_path = join(cfg.FILE_UPLOADS.PARENT_FOLDER, cfg.FILE_UPLOADS.TEMP_FOLDER)

if not exists(tmp_path):
    makedirs(tmp_path)
cfg.FILE_UPLOADS.TEMP_FOLDER = tmp_path

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=False,
    REMEMBER_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_DOMAIN=cfg.COOKIE_DOMAIN,
    SESSION_COOKIE_PATH='/',
    MAIL_SERVER=cfg.MAIL_SERVER,
    MAIL_PORT = cfg.MAIL_PORT,
    MAIL_USERNAME = cfg.MAIL_USERNAME,
    MAIL_PASSWORD = cfg.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER = cfg.MAIL_DEFAULT_SENDER,
    MAX_CONTENT_LENGTH=cfg.MAX_FILE_SIZE,
)

app.register_blueprint(accounts.bp)
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)
app.register_blueprint(tasks.bp)
app.register_blueprint(reports.bp)

add_error_handlers(app)
Request.on_json_loading_failed = on_json_loading_failed

CORS(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user_loader)

def run():
    monkey.patch_all(ssl=False)
    logger = logging.getLogger('gevent') if cfg.DISABLE_EXISTING_LOGGERS is False else None
    http_server = WSGIServer(
        (cfg.HOST, cfg.PORT),
        app,
        log = logger, # Gevent игнорирует конфигурацию логгеров, поэтому ему отедльно нужно сказать, чтобы перестал это делать
        error_log = logger
    )
    logging.info('Started server')
    http_server.serve_forever()
