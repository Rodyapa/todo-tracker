from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from todo_tracker.db.crud import user_crud
from todo_tracker.dependencies.db_dependencies import get_session
from todo_tracker.schemas.user_schemas import UserRead

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

'''
@router.post('/login', status_code=200,
             response_model=)

@router.post('/refresh', status_code=201,
             response_model=)
'''
