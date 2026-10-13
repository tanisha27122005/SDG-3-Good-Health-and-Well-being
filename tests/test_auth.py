import pytest
from auth import hash_password, verify_password, register_user

def test_password_hashing():
    pwd = "SecurePassword123!"
    hashed = hash_password(pwd)
    assert verify_password(hashed, pwd) is True
    assert verify_password(hashed, "WrongPassword") is False

def test_admin_registration_restriction():
    success, msg = register_user("fakeadmin", "Password123!", role="admin")
    assert success is False
    assert "administrator" in msg
