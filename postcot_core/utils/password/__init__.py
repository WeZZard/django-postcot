from .plaintext import (hash_plaintext_password, verify_plaintext_password)
from .md5 import (hash_md5_password, verify_md5_password)
from .crypt import (hash_crypt_password, verify_crypt_password)
from .sha import (hash_sha_password, verify_sha_password)
from .other import (hash_other_password, verify_other_password)

from .md5 import Md5Schema
from .crypt import CryptSchema
from .sha import ShaSchema
from .other import OtherSchema

from ...base_types import PasswordSchema


def verify_password(
        password: str,
        password_hash: str,
        schema: PasswordSchema
) -> bool:
    if schema == PasswordSchema.PLAIN:
        return verify_plaintext_password(password, password_hash)

    # MD5 algorithms
    if schema == PasswordSchema.PLAIN_MD5:
        return verify_md5_password(password, password_hash, Md5Schema.PLAIN)

    if schema == PasswordSchema.LDAP_MD5:
        return verify_md5_password(password, password_hash, Md5Schema.LDAP)

    if schema == PasswordSchema.SALTED_MD5:
        return verify_md5_password(password, password_hash, Md5Schema.SALTED)

    # Whatever CRYPT algorithms
    if schema == PasswordSchema.CRYPT:
        return verify_crypt_password(password, password_hash, CryptSchema.DEFAULT)

    if schema == PasswordSchema.MD5_CRYPT:
        return verify_crypt_password(password, password_hash, CryptSchema.MD5)

    if schema == PasswordSchema.SHA256_CRYPT:
        return verify_crypt_password(password, password_hash, CryptSchema.SHA256)

    if schema == PasswordSchema.SHA512_CRYPT:
        return verify_crypt_password(password, password_hash, CryptSchema.SHA512)

    if schema == PasswordSchema.BLF_CRYPT:
        return verify_crypt_password(password, password_hash, CryptSchema.BLF)

    # SHA algorithms
    if schema == PasswordSchema.SHA:
        return verify_sha_password(password, password_hash, ShaSchema.SHA, False)

    if schema == PasswordSchema.SHA256:
        return verify_sha_password(password, password_hash, ShaSchema.SHA256, False)

    if schema == PasswordSchema.SHA512:
        return verify_sha_password(password, password_hash, ShaSchema.SHA512, False)

    if schema == PasswordSchema.SALTED_SHA:
        return verify_sha_password(password, password_hash, ShaSchema.SHA, True)

    if schema == PasswordSchema.SALTED_SHA256:
        return verify_sha_password(password, password_hash, ShaSchema.SHA256, True)

    if schema == PasswordSchema.SALTED_SHA512:
        return verify_sha_password(password, password_hash, ShaSchema.SHA512, True)

    # PBKDF2 Algorithm
    if schema == PasswordSchema.PBKDF2:
        return verify_other_password(password, password_hash, OtherSchema.PBKDF2)

    raise ValueError('Unsupported password encrypt schema: %s' % schema)


def hash_password(password: str, schema: PasswordSchema) -> str:
    if schema == PasswordSchema.PLAIN:
        return hash_plaintext_password(password)

    # MD5 algorithms
    if schema == PasswordSchema.PLAIN_MD5:
        return hash_md5_password(password, Md5Schema.PLAIN)

    if schema == PasswordSchema.LDAP_MD5:
        return hash_md5_password(password, Md5Schema.LDAP)

    if schema == PasswordSchema.SALTED_MD5:
        return hash_md5_password(password, Md5Schema.SALTED)

    # Whatever CRYPT algorithms
    if schema == PasswordSchema.CRYPT:
        return hash_crypt_password(password, CryptSchema.DEFAULT)

    if schema == PasswordSchema.MD5_CRYPT:
        return hash_crypt_password(password, CryptSchema.MD5)

    if schema == PasswordSchema.SHA256_CRYPT:
        return hash_crypt_password(password, CryptSchema.SHA256)

    if schema == PasswordSchema.SHA512_CRYPT:
        return hash_crypt_password(password, CryptSchema.SHA512)

    if schema == PasswordSchema.BLF_CRYPT:
        return hash_crypt_password(password, CryptSchema.BLF)

    # SHA algorithms
    if schema == PasswordSchema.SHA:
        return hash_sha_password(password, ShaSchema.SHA, False)

    if schema == PasswordSchema.SHA256:
        return hash_sha_password(password, ShaSchema.SHA256, False)

    if schema == PasswordSchema.SHA512:
        return hash_sha_password(password, ShaSchema.SHA512, False)

    if schema == PasswordSchema.SALTED_SHA:
        return hash_sha_password(password, ShaSchema.SHA, True)

    if schema == PasswordSchema.SALTED_SHA256:
        return hash_sha_password(password, ShaSchema.SHA256, True)

    if schema == PasswordSchema.SALTED_SHA512:
        return hash_sha_password(password, ShaSchema.SHA512, True)

    # PBKDF2 Algorithm
    if schema == PasswordSchema.PBKDF2:
        return hash_other_password(password, OtherSchema.PBKDF2)

    raise ValueError('Unsupported password encrypt schema: %s' % schema)
