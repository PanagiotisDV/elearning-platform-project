import pytest
from app.core.security import get_password_hash, verify_password


def test_long_password_hashing_and_verification():
    password = "A" * 100
    hashed = get_password_hash(password)

    assert hashed
    assert verify_password(password, hashed) is True
