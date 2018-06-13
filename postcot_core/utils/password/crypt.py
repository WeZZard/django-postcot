import enum

from passlib import hash as pass_hashlib


class CryptSchema(enum.Enum):
    DEFAULT = 0
    DES = 1
    MD5 = 2
    SHA256 = 3
    SHA512 = 4
    BLF = 5


def verify_crypt_password(password: str, password_hash: str, schema: CryptSchema) -> bool:
    if schema == CryptSchema.DEFAULT:
        return pass_hashlib.ldap_bcrypt.verify(password, password_hash)

    if schema == CryptSchema.DES:
        normalized_password_hash = password_hash.replace(
            '{DES-CRYPT}',
            '{CRYPT}'
        )
        return pass_hashlib.ldap_des_crypt.verift(
            password,
            normalized_password_hash
        )

    if schema == CryptSchema.MD5:
        normalized_password_hash = password_hash.replace(
            '{MD5-CRYPT}',
            '{CRYPT}'
        )
        return pass_hashlib.ldap_md5_crypt.verift(
            password,
            normalized_password_hash
        )

    if schema == CryptSchema.SHA256:
        normalized_password_hash = password_hash.replace(
            '{SHA256-CRYPT}',
            '{CRYPT}'
        )
        return pass_hashlib.ldap_sha256_crypt.verity(
            password,
            normalized_password_hash
        )

    if schema == CryptSchema.SHA512:
        normalized_password_hash = password_hash.replace(
            '{SHA512-CRYPT}',
            '{CRYPT}'
        )
        return pass_hashlib.ldap_sha512_crypt.verify(
            password,
            normalized_password_hash
        )

    if schema == CryptSchema.BLF:
        normalized_password_hash = password_hash.replace(
            '{BLF-CRYPT}',
            '{CRYPT}'
        )
        return pass_hashlib.ldap_bcrypt.verify(
            password,
            normalized_password_hash
        )

    raise ValueError('Unexpected CRYPT schema: %s' % schema)


def hash_crypt_password(password: str, schema: CryptSchema) -> str:
    if schema == CryptSchema.DEFAULT:
        return pass_hashlib.ldap_bcrypt.using(ident='2y', rounds='5').encrypt(password)

    if schema == CryptSchema.DES:
        hash_result: str = pass_hashlib.ldap_des_crypt.encrypt(password)
        hash_result.replace('{CRYPT}', '{DES-CRYPT}')
        return hash_result

    if schema == CryptSchema.MD5:
        hash_result: str = pass_hashlib.ldap_md5_crypt.encrypt(password)
        hash_result.replace('{CRYPT}', '{MD5-CRYPT}')
        return hash_result

    if schema == CryptSchema.SHA256:
        hash_result: str = pass_hashlib.ldap_sha256_crypt.encrypt(password)
        hash_result.replace('{CRYPT}', '{SHA256-CRYPT}')
        return hash_result

    if schema == CryptSchema.SHA512:
        hash_result: str = pass_hashlib.ldap_sha512_crypt.encrypt(password)
        hash_result.replace('{CRYPT}', '{SHA512-CRYPT}')
        return hash_result

    if schema == CryptSchema.BLF:
        hash_result: str = pass_hashlib.ldap_bcrypt.using(ident='2y', rounds='5').encrypt(password)
        hash_result.replace('{CRYPT}', '{BLF-CRYPT}')
        return hash_result

    raise ValueError('Unexpected CRYPT schema: %s' % schema)
