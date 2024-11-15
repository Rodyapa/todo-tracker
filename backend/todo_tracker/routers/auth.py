from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from todo_tracker.db.crud import user_crud
from todo_tracker.dependencies.db_dependencies import get_session
from todo_tracker.redis.redis_config import get_redis_client
from todo_tracker.schemas.jwt_token_schemas import JWTTokens, RefreshToken
from todo_tracker.schemas.user_schemas import UserRead
from todo_tracker.utils.auth import authenticate_user
from todo_tracker.utils.jwt import (create_access_token, create_refresh_token,
                                    token_settings, verify_token)

router = APIRouter(
    prefix='/auth',
    tags=['Auth', ]
)


@router.post('/register', status_code=201,
             response_model=UserRead)
async def create_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session)
):
    db_user = await user_crud.create_user(user=user_data,
                                          session=session)
    return db_user


@router.post('/login', status_code=200,
             response_model=JWTTokens)
async def create_token(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
    redis_client: Redis = Depends(get_redis_client)
) -> JWTTokens:
    user = await authenticate_user(
        db=session,
        username=user_data.username,
        password=user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = await create_access_token(data={"sub": user.username, })
    refresh_token = await create_refresh_token(data={"sub": user.username, })

    await redis_client.setex(
        user.username,
        timedelta(days=token_settings.REFRESH_TOKEN_EXPIRE_DAYS),
        refresh_token
    )
    return {"access_token": access_token, "refresh_token": refresh_token,
            "token_type": "bearer"}


@router.post("/refresh", status_code=200,
             response_model=JWTTokens)
async def refresh_token(
        token: RefreshToken,
        redis_client: Redis = Depends(get_redis_client)):
    '''Returns new access token if valid refresh token was provided.
    Returns:
        JWTTokens: access token, refresh token and token type.

    Raises:
        HTTPException: If token validation fails,
        raises a 401 Unauthorized error.'''
    payload = await verify_token(
        token=token.refresh_token,
        secret_key=token_settings.JWT_REFRESH_SECRET_KEY)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid refresh token")

    saved_token = await redis_client.get(payload["sub"])
    if saved_token != token.refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired refresh token")
    new_access_token = await create_access_token({"sub": payload["sub"]})

    return {"access_token": new_access_token,
            "refresh_token": refresh_token.refresh_token,
            "token_type": "bearer"}
