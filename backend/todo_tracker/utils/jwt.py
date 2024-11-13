from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from todo_tracker.config import JWTSettings

token_settings = JWTSettings()


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=token_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_settings.JWT_SECRET_KEY,
                             algorithm=token_settings.JWT_ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=token_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             token_settings.JWT_REFRESH_SECRET_KEY,
                             algorithm=token_settings.JWT_ALGORITHM)
    return encoded_jwt


async def verify_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key,
                             algorithms=[token_settings.JWT_ALGORITHM, ])
        return payload if "sub" in payload else None
    except InvalidTokenError:
        return None