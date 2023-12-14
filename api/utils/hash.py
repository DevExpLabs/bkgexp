import hashlib


def hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf8")).hexdigest()
