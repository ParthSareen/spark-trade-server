import datetime
import re
from typing import Optional
import bcrypt
import jwt


def validate_username(username: str) -> bool:
    """Validate a username against a regex pattern."""
    pattern = r"^[a-zA-Z0-9_-]{3,20}$"
    return bool(re.match(pattern, username))


def validate_name(name: str) -> bool:
    """Check if the name is within acceptable length."""
    return 1 < len(name) < 100


def validate_email(email: str) -> bool:
    """Validate an email address against a regex pattern."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(pattern, email))


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    """Check if a password matches its hash."""
    return bcrypt.checkpw(password.encode(), hashed_password)


def token_encode(username: str, key: str, expiry_days: float) -> str:
    """Encode a JWT token."""
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(days=expiry_days)
    return jwt.encode({'username': username, 'exp': exp_date}, key, algorithm='HS256')


def token_decode(token: str, key: str) -> Optional[dict]:
    """Decode a JWT token."""
    try:
        return jwt.decode(token, key, algorithms=['HS256'], options={"verify_exp": True})
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
