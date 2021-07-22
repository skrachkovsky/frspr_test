from . import *  # noqa

DEBUG = True

LOGGING['loggers']['']['handlers'] = ['stream' ]  # noqa
LOGGING['loggers']['']['level'] = 'DEBUG'  # noqa
