import hashlib


class Hashing:
    def __init__(self):
        pass

    def hash_password(password: str) -> str:
        sha = hashlib.sha256()
        sha.update(password.encode())
        return sha.hexdigest()