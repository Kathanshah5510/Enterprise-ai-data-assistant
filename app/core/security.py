from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import jwt

from app.core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS: int = 7


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def _build_token(payload: dict[str, Any]) -> str:
    if not settings.SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured.")
    if not settings.ALGORITHM:
        raise RuntimeError("ALGORITHM is not configured.")
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _build_token({"sub": subject, "exp": expire, "type": "access"})


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _build_token({"sub": subject, "exp": expire, "type": "refresh"})


def decode_token(token: str) -> dict[str, Any]:
    if not settings.SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured.")
    if not settings.ALGORITHM:
        raise RuntimeError("ALGORITHM is not configured.")
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
