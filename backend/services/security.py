import hashlib
import os

_PEPPER = os.getenv("POST_PASSWORD_PEPPER", "tour-community-default-pepper")


def hash_password(password: str) -> str:
    return hashlib.sha256(f"{_PEPPER}:{password}".encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash
