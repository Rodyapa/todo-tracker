from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class JWTTokens(AccessToken, RefreshToken):
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
