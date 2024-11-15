from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from todo_tracker.db.crud.user_crud import get_user_by_username
from todo_tracker.db.models.user import User
from todo_tracker.dependencies.db_dependencies import get_session
from todo_tracker.schemas.jwt_token_schemas import TokenData
from todo_tracker.utils.jwt import token_settings, verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(
          token: str = Depends(oauth2_scheme),
          db: AsyncSession = Depends(get_session)) -> User:
    """
    Retrieves the current authenticated user based on a JWT token.

    Args:
        token (str): JWT token provided by the user for authentication.
        db (AsyncSession): Database session used to retrieve user information.

    Returns:
        User: The authenticated user associated with the token.

    Raises:
        HTTPException: If token validation fails or user is not found,
        raises a 401 Unauthorized error
        with a 'Bearer' WWW-Authenticate header.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = await verify_token(token, token_settings.JWT_SECRET_KEY)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')
    username: str = payload.get('sub')
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)
    user = await get_user_by_username(session=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
