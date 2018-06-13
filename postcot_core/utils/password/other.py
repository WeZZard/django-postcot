from passlib import hash as pass_hashlib

import enum


class OtherSchema(enum.Enum):
    PBKDF2 = 0


def verify_other_password(password: str, password_hash: str, schema: OtherSchema) -> bool:
    if schema == OtherSchema.PBKDF2:
        raise NotImplemented()

    raise ValueError('Unexpected other schema: %s' % schema)


def hash_other_password(password: str, schema: OtherSchema) -> str:
    if schema == OtherSchema.PBKDF2:
        raise NotImplemented()

    raise ValueError('Unexpected other schema: %s' % schema)
