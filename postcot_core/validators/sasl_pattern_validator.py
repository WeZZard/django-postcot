from django.core import exceptions
from django.core import validators

from .username_pattern_validator import UsernamePatternValidator


@validators.deconstructible
class SaslPatternValidator:
    def __call__(self, value: str):
        try:
            validators.EmailValidator()(value)
        except exceptions.ValidationError:
            try:
                UsernamePatternValidator()(value)
            except exceptions.ValidationError:
                raise '%s is not a valid email address pattern nor username.' % value

    def __eq__(self, other):
        return isinstance(other, SaslPatternValidator)
