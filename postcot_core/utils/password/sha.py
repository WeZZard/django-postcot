import re
import enum

from passlib import hash as pass_hashlib
from passlib.handlers.ldap_digests import _SaltedBase64DigestHelper
from passlib.utils.compat import u
from hashlib import sha256, sha512
import binascii
import base64


class ldap_salted_sha256(_SaltedBase64DigestHelper):
    name = "ldap_salted_sha256"
    ident = u("{SSHA256}")
    checksum_size = 32
    _hash_func = sha256
    _hash_regex = re.compile(u(r"^\{SSHA256\}(?P<tmp>[+/a-zA-Z0-9]{32,}={0,2})$"))


class ldap_salted_sha512(_SaltedBase64DigestHelper):
    name = "ldap_salted_sha512"
    ident = u("{SSHA512}")
    checksum_size = 64
    _hash_func = sha512
    _hash_regex = re.compile(u(r"^\{SSHA512\}(?P<tmp>[+/a-zA-Z0-9]{32,}={0,2})$"))


class ShaSchema(enum.Enum):
    SHA = 0
    SHA256 = 1
    SHA512 = 2


def verify_sha_password(password: str, password_hash: str, schema: ShaSchema, salted: bool) -> bool:
    if schema == ShaSchema.SHA:
        if salted:
            return pass_hashlib.ldap_salted_sha1.verify(password, password_hash)
        else:
            normalized_password_hash = binascii.hexlify(
                base64.b64decode(
                    password_hash.strip('{SHA}').encode()
                )
            ).decode()

            return pass_hashlib.hex_sha1.verify(password, normalized_password_hash)

    if schema == ShaSchema.SHA256:
        if salted:
            return ldap_salted_sha256.verify(password, password_hash)
        else:
            normalized_password_hash = binascii.hexlify(
                base64.b64decode(
                    password_hash.strip('{SHA256}').encode()
                )
            ).decode()

            return pass_hashlib.hex_sha256.verify(password, normalized_password_hash)

    if schema == ShaSchema.SHA512:
        if salted:
            return ldap_salted_sha512.verify(password, password_hash)
        else:
            normalized_password_hash = binascii.hexlify(
                base64.b64decode(
                    password_hash.strip('{SHA512}').encode()
                )
            ).decode()

            return pass_hashlib.hex_sha512.verify(password, normalized_password_hash)

    raise ValueError('Unexpected SHA schema: %s, salted %s' % (schema, salted))


def hash_sha_password(password: str, schema: ShaSchema, salted: bool) -> str:
    if schema == ShaSchema.SHA:
        if salted:
            return pass_hashlib.ldap_salted_sha1.hash(password)
        else:
            primitive_hash = pass_hashlib.hex_sha1.hash(password)
            unhexilified_hash = binascii.unhexlify(primitive_hash)
            base64_hash = binascii.b2a_base64(unhexilified_hash).decode()
            return '{SHA}%s' % base64_hash

    if schema == ShaSchema.SHA256:
        if salted:
            return ldap_salted_sha256.hash(password)
        else:
            primitive_hash = pass_hashlib.hex_sha256.hash(password)
            unhexilified_hash = binascii.unhexlify(primitive_hash)
            base64_hash = binascii.b2a_base64(unhexilified_hash).decode()
            return '{SHA256}%s' % base64_hash

    if schema == ShaSchema.SHA512:
        if salted:
            return ldap_salted_sha512.hash(password)
        else:
            primitive_hash = pass_hashlib.hex_sha512.hash(password)
            unhexilified_hash = binascii.unhexlify(primitive_hash)
            base64_hash = binascii.b2a_base64(unhexilified_hash).decode()
            return '{SHA512}%s' % base64_hash

    raise ValueError('Unexpected SHA schema: %s, salted %s' % (schema, salted))
