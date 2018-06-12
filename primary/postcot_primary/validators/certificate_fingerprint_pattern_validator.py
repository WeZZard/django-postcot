import re

from django.core import validators


@validators.deconstructible
class CertificateFingerprintPatternValidator(validators.RegexValidator):
    def __init__(self):
        super(CertificateFingerprintPatternValidator, self).__init__(
            regex=r'^([A-Fa-f0-9]{2}:)+[A-Fa-f0-9]{2}$',
            message='Not a valid fingerprint.',
            flags=re.IGNORECASE
        )
