from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from todo_tracker.config import JWTSettings

token_settings = JWTSettings()


async def create_access_token(data: dict) -> str:
    """
    Creates a JWT access token with a specific expiration time.

    Args:
        data (dict): A dictionary containing the data to encode in the token.

    Returns:
        str: The encoded JWT access token.

    The token includes an expiration time calculated based on the
    `ACCESS_TOKEN_EXPIRE_MINUTES` setting in `JWTSettings`.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=token_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_settings.JWT_SECRET_KEY,
                             algorithm=token_settings.JWT_ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict) -> str:
    """
    Creates a JWT refresh token with a specific expiration time.

    Args:
        data (dict): A dictionary containing the data to encode in the token.

    Returns:
        str: The encoded JWT refresh token.

    The token includes an expiration time calculated based on the
    `REFRESH_TOKEN_EXPIRE_DAYS` setting in `JWTSettings`.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=token_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             token_settings.JWT_REFRESH_SECRET_KEY,
                             algorithm=token_settings.JWT_ALGORITHM)
    return encoded_jwt


async def verify_token(token: str, secret_key: str) -> dict | None:
    """
    Verifies and decodes a JWT token.

    Args:
        token (str): The JWT token to verify.
        secret_key (str): The secret key used to decode the token.

    Returns:
        dict | None: The payload of the token if valid and
        contains a "sub" claim,
        otherwise `None`.

    Raises:
        None: If the token is invalid, the function silently returns `None`.
    """
    try:
        payload = jwt.decode(token, secret_key,
                             algorithms=[token_settings.JWT_ALGORITHM, ])
        return payload if "sub" in payload else None
    except InvalidTokenError:
        return None
