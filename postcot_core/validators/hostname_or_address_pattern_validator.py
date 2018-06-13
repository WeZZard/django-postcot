import re

from django.core import validators

from ..constants import (
    IPV4_ADDRESS_PATTERN,
    IPV6_ADDRESS_PATTERN,
    IPV4_NETWORK_PATTERN,
    IPV6_NETWORK_PATTERN,
    DOMAIN_PATTERN,
)


@validators.deconstructible
class HostnameOrAddressPatternValidator(validators.RegexValidator):
    def __init__(self):
        patterns = [
            DOMAIN_PATTERN,
            '\.%s' % DOMAIN_PATTERN,
            IPV4_ADDRESS_PATTERN,
            IPV6_ADDRESS_PATTERN,
            IPV4_NETWORK_PATTERN,
            IPV6_NETWORK_PATTERN,
        ]

        pattern = '|'.join(['(^%s$)' % p for p in patterns])

        super(HostnameOrAddressPatternValidator, self).__init__(
            regex=r'%s' % pattern,
            message='Not a valid hostname, domain, subdomain, IP address nor network.',
            flags=re.IGNORECASE | re.VERBOSE
        )
