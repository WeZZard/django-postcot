from .base import *

DEBUG = False

_DB_HOST: str = os.environ.get('POSTCOT_PGSQL_DB_HOST')
if _DB_HOST is None or len(_DB_HOST) == 0:
    _DB_HOST = 'localhost'  # Default host

_DB_PORT: str = os.environ.get('POSTCOT_PGSQL_DB_PORT')
if _DB_PORT is None or len(_DB_PORT) == 0:
    _DB_PORT = ''  # Default port

_DB_NAME: str = os.environ.get('POSTCOT_PGSQL_DB_NAME')
if _DB_NAME is None or len(_DB_NAME) == 0:
    raise ValueError('Invalid value for environment variable POSTCOT_PGSQL_DB_NAME: {}'.format(_DB_NAME))

_DB_USER: str = os.environ.get('POSTCOT_PGSQL_DB_USER')
if _DB_USER is None or len(_DB_USER) == 0:
    raise ValueError('Invalid value for environment variable POSTCOT_PGSQL_DB_USER: {}'.format(_DB_USER))

_DB_PASSWORD: str = os.environ.get('POSTCOT_PGSQL_DB_PASSWORD')
if _DB_PASSWORD is None or len(_DB_PASSWORD) == 0:
    raise ValueError('Invalid value for environment variable POSTCOT_PGSQL_DB_PASSWORD: {}'.format(_DB_PASSWORD))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': _DB_NAME,
        'USER': _DB_USER,
        'PASSWORD': _DB_PASSWORD,
        'HOST': _DB_HOST,
        'PORT': _DB_PORT,
    }
}
