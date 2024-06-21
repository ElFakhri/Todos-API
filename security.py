from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# secret_key = secrets.token_urlsafe(32)
secret_key = "secret"


def create_token(username):
    exp = datetime.now() + timedelta(days=1)
    to_encode = {"exp": exp, "sub": username}
    encoded = jwt.encode(to_encode, secret_key, algorithm="HS256")

    return encoded
