"""Random short-code generation."""

import secrets
import string


def generate_base62_secret(length=6):
    """Generate a random base62 (digits + upper/lowercase letters) string.

    Args:
        length: number of characters to generate.

    Returns:
        A random base62 string of the given length.
    """
    alphabet = string.digits + string.ascii_letters
    return "".join(secrets.choice(alphabet) for _ in range(length))
