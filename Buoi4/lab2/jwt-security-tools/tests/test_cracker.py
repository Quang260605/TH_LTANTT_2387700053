import jwt
import tempfile
from jwt_cracker.cracker import JWTCracker

def test_crack_token():
    secret = "s3cret"
    token = jwt.encode({"sub": "test"}, secret, algorithm="HS256")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write("wrongpass\n123456\ns3cret\n")
        f.seek(0)
        cracker = JWTCracker(token, f.name)
        found = cracker.crack()

    assert found == secret
