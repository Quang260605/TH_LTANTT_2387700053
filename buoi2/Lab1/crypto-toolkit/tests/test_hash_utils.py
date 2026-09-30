import pytest
from securecrypto import hash_utils
from argon2.exceptions import VerifyMismatchError

def test_hash_password_and_verify():
    pwd_input = ""
    hashed = hash_utils.hash_password_secure(pwd_input)
    assert hashed is not None

    from argon2 import PasswordHasher
    ph = PasswordHasher()
    try:
        ph.verify(hashed, pwd_input)
        verified = True
    except VerifyMismatchError:
        verified = False
        
    assert verified == True

def test_wrong_password_verification():
    pwd_input = "CorrectPass"
    wrong_pwd_input = "WrongPass"
    hashed = hash_utils.hash_password_secure(pwd_input)

    from argon2 import PasswordHasher
    ph = PasswordHasher()
    try:
        ph.verify(hashed, wrong_pwd_input)
        verified = True
    except VerifyMismatchError:
        verified = False
        
    assert verified == False
