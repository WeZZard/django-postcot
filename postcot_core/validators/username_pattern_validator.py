import re

from django.core import validators

from ..constants import USERNAME_PATTERN


@validators.deconstructible
class UsernamePatternValidator(validators.RegexValidator):
    def __init__(self):
        super(UsernamePatternValidator, self).__init__(
            regex=r'^%s$' % USERNAME_PATTERN,
            message='Invalid username.',
            flags=re.IGNORECASE | re.VERBOSE
        )
