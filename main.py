from argparse import ArgumentParser
import logging
import urllib3
import bcrypt
import logging
import logging.config

import app
from app import db
from app.config import cfg
'''
Логгирование нужно конфигурировать в самом начале какой-нибудь логгер может успеть 
создаться раньше с дефольтным конфигом и начать писать логи, которые мы не хотим видеть
Если перенести это вглубь приложение все может сломаться
Но это не точно (с)
'''
logging.config.dictConfig(cfg.LOGGING)

if cfg.DISABLE_EXISTING_LOGGERS:
    log_level = 100
else:
    log_level = cfg.LOG_LEVEL

for name, logger in logging.root.manager.loggerDict.items():
    dot = name.rfind('.', 0, len(name[0]) - 1)
    if dot == -1:
        if not isinstance(logger, logging.PlaceHolder) and name not in cfg.LOGGING['loggers']:
            logger.setLevel(log_level)

def main():

    if log_level <= 10:
        import logging_tree
        logging_tree.printout()

    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = ArgumentParser(description='Backend service of Events project')

    parser.add_argument('--create-tables', action='store_true',
                        dest='create_tables',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()
    
    if args.create_tables:
        pw = bcrypt.hashpw(str(cfg.SUPER_ADMIN_PASSWORD).encode('utf-8'), bcrypt.gensalt())
        cfg.SUPER_ADMIN_PASSWORD = ""
        db.create_tables(pw.decode('utf-8'))

    logging.info('Starting restful api backend server')
    logging.info('IP: ' + cfg.HOST + '  PORT: ' + str(cfg.PORT))
    app.run()


if __name__ == '__main__':
    main()
