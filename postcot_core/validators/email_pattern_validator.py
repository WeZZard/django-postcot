import re

from django.core import validators

from ..constants import (
    EMAIL_PATTERN,
    USERNAME_PATTERN,
    DOMAIN_PATTERN,
)


@validators.deconstructible
class EmailPatternValidator(validators.RegexValidator):
    def __init__(self):
        patterns = [
            EMAIL_PATTERN,
            DOMAIN_PATTERN,
            '\.%s' % DOMAIN_PATTERN,
            USERNAME_PATTERN
        ]

        pattern = '|'.join(['(^%s$)' % p for p in patterns])

        super().__init__(
            regex=r'%s' % pattern,
            message='Not a valid email pattern.',
            flags=re.IGNORECASE | re.VERBOSE
        )
