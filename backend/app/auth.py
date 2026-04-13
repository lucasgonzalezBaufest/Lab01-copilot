from datetime import datetime, timedelta, timezone
from typing import Optional
import os

import bcrypt
from jose import JWTError, jwt

# Load from environment variable; fail loudly if not set in production.
# A default is provided only for local development convenience.
SECRET_KEY: str = os.getenv(
    "SECRET_KEY",
    "change-me-in-production-use-a-long-random-secret",
)
if SECRET_KEY == "change-me-in-production-use-a-long-random-secret":
    import warnings
    warnings.warn(
        "SECRET_KEY is using the insecure default. "
        "Set the SECRET_KEY environment variable before deploying to production.",
        stacklevel=1,
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 3600

# Pre-computed bcrypt hash for the admin password "admin123".
# To regenerate: python -c "import bcrypt; print(bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode())"
_ADMIN_HASHED_PW: bytes = b"$2b$12$uPB3lRE89HV2SWe50wtcQO/ReXGBCOmZ10z./BACysgG5OH3ShvHG"

# Fake user database (replace with a real database in production)
FAKE_USERS: dict = {
    "admin": {
        "username": "admin",
        "hashed_password": _ADMIN_HASHED_PW,
    }
}


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = FAKE_USERS.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_SECONDS) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: int = REFRESH_TOKEN_EXPIRE_SECONDS) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
