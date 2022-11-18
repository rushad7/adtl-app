from hashlib import sha256


def encrypt(password: str) -> str:
    password_encrypted = sha256(password.encode("utf-8")).hexdigest()
    return password_encrypted
