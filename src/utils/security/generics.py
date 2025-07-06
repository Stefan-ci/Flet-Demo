from utils.settings import PASSWORD_HASH_MECHANISM


def hash_str(secret: str):
    return PASSWORD_HASH_MECHANISM.hash(secret=secret)


def check_hash(hashed_str: str, input: str) -> bool:
    return PASSWORD_HASH_MECHANISM.verify(secret=input, hash=hashed_str)


def needs_rehash(hashed_str: str):
    return PASSWORD_HASH_MECHANISM.needs_update(hashed_str)
