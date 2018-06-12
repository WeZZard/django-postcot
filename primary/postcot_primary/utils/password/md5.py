import enum

from passlib import hash as pass_hashlib


class Md5Schema(enum.Enum):
    PLAIN = 0
    LDAP = 1
    SALTED = 2


def verify_md5_password(password: str, password_hash: str, schema: Md5Schema) -> bool:
    if schema == Md5Schema.PLAIN:
        normalized_password_hash = password_hash.replace('{PLAIN-MD5}', '{MD5}')
        return pass_hashlib.ldap_hex_md5.verify(password, normalized_password_hash)

    if schema == Md5Schema.LDAP:
        normalized_password_hash = password_hash.replace('{LDAP-MD5}', '{MD5}')
        return pass_hashlib.ldap_md5.verify(password, normalized_password_hash)

    if schema == Md5Schema.SALTED:
        return pass_hashlib.ldap_salted_md5.verify(password, password_hash)

    raise ValueError('Unexpected MD5 schema: %s' % schema)


def hash_md5_password(password: str, schema: Md5Schema) -> str:
    if schema == Md5Schema.PLAIN:
        hash_result: str = pass_hashlib.ldap_hex_md5.encrypt(password)
        hash_result.replace('{MD5}', '{PLAIN-MD5}')
        return hash_result

    if schema == Md5Schema.LDAP:
        hash_result: str = pass_hashlib.ldap_md5.encrypt(password)
        hash_result.replace('{MD5}', '{LDAP-MD5}')
        return hash_result

    if schema == Md5Schema.SALTED:
        return pass_hashlib.ldap_salted_md5.hash(password)

    raise ValueError('Unexpected MD5 schema: %s' % schema)
