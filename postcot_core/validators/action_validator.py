import re

from django.core import validators
from ..constants import ACTION_PATTERN


@validators.deconstructible()
class ActionValidator(validators.RegexValidator):
    def __init__(self):
        super(ActionValidator, self).__init__(
            regex=r'^(%s)$' % ACTION_PATTERN,
            message='Invalid action.',
            flags=re.VERBOSE
        )
