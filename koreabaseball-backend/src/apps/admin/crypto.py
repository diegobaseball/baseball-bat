from config import (
    SECRET_KEY,
    REFRESH_SECRET_KEY,
    ARGON2_MEMORY_COST,
    ARGON2_PARALLELISM,
    ARGON2_SALT_SIZE,
    ARGON2_TIME_COST,
)
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = SECRET_KEY
JWT_REFRESH_SECRET_KEY = REFRESH_SECRET_KEY

password_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=ARGON2_MEMORY_COST,  # Memory cost (in kibibytes)
    argon2__time_cost=ARGON2_TIME_COST,  # Number of iterations
    argon2__parallelism=ARGON2_PARALLELISM,  # Number of threads
    argon2__salt_size=ARGON2_SALT_SIZE,  # Salt size (in bytes, default is 16)
)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(
    subject: Union[str, Any], uuid: str, expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta

    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject), "uuid": uuid}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], uuid: str, expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject), "uuid": uuid}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
