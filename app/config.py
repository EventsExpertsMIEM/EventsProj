from types import SimpleNamespace
import os

from app import logging_config

cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)

def _get_number(env):
    return int(os.getenv(env))
    
cfg.CSRF_ENABLED = False if os.getenv('DISABLE_CSRF') else True
cfg.SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
cfg.HOST = os.getenv('HOST_ADDR', '0.0.0.0')
cfg.PORT = int(os.getenv('PORT', '8080'))
cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.RUNTIME_FOLDER = os.path.dirname(os.path.abspath(__file__))
cfg.SCRIPTS_FOLDER = os.getenv('SCRIPT_FOLDER', '{}/scripts'.format(cfg.RUNTIME_FOLDER))

cfg.COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', '')

cfg.SUPER_ADMIN_MAIL = os.getenv('SUPER_ADMIN_MAIL')
cfg.SUPER_ADMIN_PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')
cfg.DEFAULT_USER_STATUS = os.getenv('DEFAULT_USER_STATUS')
cfg.MAKE_ALL_LOGS = os.getenv('MAKE_ALL_LOGS', False)

cfg.SITE_ADDR = os.getenv('SITE_ADDR')

cfg.MAIL_SERVER = os.getenv('MAIL_SERVER')
cfg.MAIL_PORT = os.getenv('MAIL_PORT')
cfg.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
cfg.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
cfg.MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

cfg.LOG_LEVEL = logging_config.LOG_LEVEL
cfg.LOGGING = logging_config.LOGGING
cfg.DISABLE_EXISTING_LOGGERS = logging_config.DISABLE_EXISTING_LOGGERS

cfg.MAX_FILE_SIZE = _get_number('MAX_FILE_SIZE') * 1024 * 1024 # Глобальный максимальны размер файла, которы фласк может переварить
cfg.FILE_UPLOADS = SimpleNamespace()
cfg.FILE_UPLOADS.PARENT_FOLDER = os.getenv('FILE_UPLOADS_PARENT_FOLDER')
cfg.FILE_UPLOADS.TEMP_FOLDER = 'tmp'
cfg.FILE_UPLOADS.FILE_SETS = {
                                'AVATAR': SimpleNamespace(),
                                'REPORT': SimpleNamespace()
                            }
avatars = cfg.FILE_UPLOADS.FILE_SETS['AVATAR']
avatars.FOLDER = 'avatars'
avatars.MAX_SIZE =  8 * 1024 * 1024 # Максимальный размер аватара 8 Мб, спизженно у дискорда,
avatars.ALLOWED_EXTENSIONS = ('jpg', 'png')
avatars.ALLOWED_MIME_TYPES = ('image/jpeg', 'image/jpg', 'image/png')

reports = cfg.FILE_UPLOADS.FILE_SETS['REPORT']
reports.FOLDER = 'reports'
reports.ALLOWED_EXTENSIONS = ('doc', 'docx', 'ppt', 'pptx', 'pdf')
reports.ALLOWED_MIME_TYPES = (
                                'application/msword',
                                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                'application/vnd.ms-powerpoint',
                                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                                'application/pdf'
                            )
reports.MAX_SIZE = cfg.MAX_FILE_SIZE
