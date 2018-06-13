from typing import List

import re

from django.core import validators
from ..constants import IPV4_ADDRESS_PATTERN, IPV6_ADDRESS_PATTERN


# Flags
IPv4 = 0b1
IPv6 = 0b1 << 1


@validators.deconstructible
class IpAddressValidator(validators.RegexValidator):
    def __init__(self, flags: int=(IPv4 | IPv6)):
        patterns: List[str] = []

        if (flags & IPv4) != 0:
            patterns.append(IPV4_ADDRESS_PATTERN)
        if (flags & IPv6) != 0:
            patterns.append(IPV6_ADDRESS_PATTERN)

        pattern = '|'.join(['(^%s$)' % p for p in patterns])

        super(IpAddressValidator, self).__init__(
            regex=r'%s' % pattern,
            message='Invalid IP address.',
            flags=re.IGNORECASE | re.VERBOSE
        )
