import os

log_levels = {
    'DISABLED': 9000,
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}

log_level = os.getenv('LOG_LEVEL')

if log_level:
    try:
        LOG_LEVEL = int(log_level)
    except:
        try:
            LOG_LEVEL = log_levels[log_level.upper()]
        except:
            LOG_LEVEL = 0
else:
    LOG_LEVEL = 0

disable_log = os.getenv('DISABLE_EXISTING_LOGGERS')
if disable_log:
    if disable_log.lower() == 'true':
        DISABLE_EXISTING_LOGGERS = True
    elif disable_log.lower() == 'false':
        DISABLE_EXISTING_LOGGERS = False
else:
    DISABLE_EXISTING_LOGGERS = False

LOGGING = { 
    'version': 1,
    'disable_existing_loggers': DISABLE_EXISTING_LOGGERS,
    'incremental': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': LOG_LEVEL
        },
    },
    'root': {
        'handlers': ['default'],
        'level': LOG_LEVEL
    },
    'loggers': { 
        # 'requests': {  # root logger
        #     'handlers': ['default'],
        #     'propagate': True,
        #     'level': 500
        # },
    }
}