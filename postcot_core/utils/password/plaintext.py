from passlib import hash as pass_hashlib


def verify_plaintext_password(password: str, password_hash: str) -> bool:
    normalized_password_hash = password_hash.strip('{PLAIN}')
    return pass_hashlib.plaintext.verify(password, normalized_password_hash)


def hash_plaintext_password(password: str) -> str:
    hash_result: str = pass_hashlib.plaintext.encrypt(password)
    hash_result = '{PLAIN}%s' % hash_result
    return hash_result
