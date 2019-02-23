from .base import *

import django_heroku
django_heroku.settings(locals())
TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'
