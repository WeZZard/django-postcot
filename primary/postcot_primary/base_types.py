from typing import Type
from typing import Optional
from typing import Callable
from typing import NoReturn

from .validators import (
    CertificateFingerprintPatternValidator,
    HostnameOrAddressPatternValidator,
    IpAddressValidator,
    SaslPatternValidator
)

import enumfields


class AccessControlRole(enumfields.Enum):
    CLIENT = 'CLIENT'
    HELO = 'HELO'
    RECIPIENT = 'RECIPIENT'
    SENDER = 'SENDER'

    class Labels:
        CLIENT = 'Client'
        HELO = 'Helo'
        RECIPIENT = 'Recipient'
        SENDER = 'Sender'


class AccessControlContent(enumfields.Enum):
    CERT = 'CERT'
    HOSTNAME = 'HOSTNAME'
    A_RECORD = 'A_RECORD'
    MX_RECORD = 'MX_RECORD'
    NS_RECORD = 'NS_RECORD'
    SASL = 'SASL'

    class Labels:
        CERT = 'Certificate Fingerprint'
        HOSTNAME = 'Hostname'
        A_RECORD = 'A Record'
        MX_RECORD = 'MX Record'
        NS_RECORD = 'NS Record'
        SASL = 'SASL'

    def pattern_validator(self) -> Optional[Type[Callable[[str], NoReturn]]]:
        if self == AccessControlContent.CERT:
            return CertificateFingerprintPatternValidator
        if self == AccessControlContent.HOSTNAME:
            return HostnameOrAddressPatternValidator
        if self == AccessControlContent.A_RECORD:
            return IpAddressValidator
        if self == AccessControlContent.MX_RECORD:
            return IpAddressValidator
        if self == AccessControlContent.NS_RECORD:
            return IpAddressValidator
        if self == AccessControlContent.SASL:
            return SaslPatternValidator
        raise ValueError('Unexpected AccessControlType value: %s' % self)


class PasswordSchema(enumfields.Enum):
    PLAIN = 'PLAIN'

    # Whatever CRYPT Algorithms
    CRYPT = 'CRYPT'
    DES_CRYPT = 'DES-CRYPT'
    MD5_CRYPT = 'MD5-CRYPT'
    SHA256_CRYPT = 'SHA256-CRYPT'
    SHA512_CRYPT = 'SHA512-CRYPT'
    BLF_CRYPT = 'BLF-CRYPT'

    # MD5 Algorithms
    PLAIN_MD5 = 'PLAIN-MD5'
    LDAP_MD5 = 'LDAP-MD5'
    SALTED_MD5 = 'SMD5'

    # SHA Algorithms
    SHA = 'SHA'
    SHA256 = 'SHA256'
    SHA512 = 'SHA512'
    SALTED_SHA = 'SSHA'
    SALTED_SHA256 = 'SSHA256'
    SALTED_SHA512 = 'SSHA512'

    # ARGON Algorithms (Not supported in FreeBSD with official ports)
    # ARGON2I = 'ARGON2I'
    # ARGON2ID = 'ARGON2ID'

    PBKDF2 = 'PBKDF2'

    def __iter__(self):
        for x in [self.value, self.label]:
            yield x

    @classmethod
    def _pad_separator_string(cls, title: str) -> str:
        title_len = len(title)
        max_len = max(list([len(each[1]) for each in super().choices()]))
        left_padding = int((max_len - title_len) / 2)
        right_padding = max_len - left_padding - title_len
        return '-' * left_padding + title + '-' * right_padding

    class Labels:
        PLAIN = 'PLAIN, password in plaintext.'

        CRYPT = 'CRYPT, default CRYPT scheme.'
        DES_CRYPT = 'DES-CRYPT, traditional DES-crypted password in /etc/passwd.'
        MD5_CRYPT = 'MD5-CRYPT, a weak but common scheme often used in /etc/shadow.'
        SHA256_CRYPT = 'SHA256-CRYPT, a strong scheme.'
        SHA512_CRYPT = 'SHA512-CRYPT, a strong scheme.'
        BLF_CRYPT = 'BLF-CRYPT, Blowfish crypt (bcrypt) scheme.'

        PLAIN_MD5 = 'PLAIN-MD5, plain MD5 sum of the password stored in hex.'
        LDAP_MD5 = 'LDAP-MD5, MD5 sum of the password stored in base64.'
        SALTED_MD5 = 'SMD5, salted MD5 sum of the password stored in base64.'

        SHA = 'SHA, SHA1 sum of the password stored in base64.'
        SHA256 = 'SHA256, SHA256 sum of the password stored in base64.'
        SHA512 = 'SHA512, SHA512 sum of the password stored in base64.'
        SALTED_SHA = 'SSHA, salted SHA1 sum of the password stored in base64.'
        SALTED_SHA256 = 'SSHA256, salted SHA256 sum of the password stored in base64.'
        SALTED_SHA512 = 'SSHA512, salted SHA512 sum of the password stored in base64.'

        PBKDF2 = 'PBKDF2, PKCS5 Password hashing algortihm.'
