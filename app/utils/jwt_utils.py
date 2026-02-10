from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm="HS256",
    )
