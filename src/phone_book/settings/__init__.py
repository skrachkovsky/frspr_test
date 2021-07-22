import os

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ROOT_DIR = os.path.dirname(BASE_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    },
    'handlers': {
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(ROOT_DIR, 'logs', 'errors.log'),
            'formatter': 'default'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

DATABASE = {
    'user': 'user',
    'database': 'db',
    'host': 'db',
    'password': 'x3u82yiCRYcAVEjjGoYLLRU5E0XK9Ini',
    'maxsize': 20
}
