"""Password generation logic."""

import secrets
import random

from .constants import CHAR_SETS


def generate_password(length: int, char_types: list[str]) -> str:
    """Generate a password with specified character types and length."""
    all_chars = "".join(CHAR_SETS[ct] for ct in char_types if ct in CHAR_SETS)

    if not all_chars:
        raise ValueError("At least one character type must be selected")

    return "".join(secrets.choice(all_chars) for _ in range(length))


def get_random_char_types() -> list[str]:
    """Randomly select character types (at least 1, up to all 4)."""
    all_types = list(CHAR_SETS.keys())
    num_types = random.randint(1, len(all_types))
    return random.sample(all_types, num_types)
