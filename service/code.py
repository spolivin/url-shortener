import secrets
import string


def generate_base62_secret(length=6):
    alphabet = string.digits + string.ascii_letters
    return "".join(secrets.choice(alphabet) for _ in range(length))
