import re

from django.core import validators

from ..constants import DOMAIN_PATTERN


@validators.deconstructible
class DomainValidator(validators.RegexValidator):
    def __init__(self):
        super(DomainValidator, self).__init__(
            regex=r'%s' % DOMAIN_PATTERN,
            message='Not a valid domain.',
            flags=re.IGNORECASE | re.VERBOSE
        )
