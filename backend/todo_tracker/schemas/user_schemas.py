import re

from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str

    @classmethod
    @field_validator('password')
    def check_password_length(cls, v):
        if len(v) < 8:
            raise ValueError('password should be at least 8 symbols long.')
        return v

    @field_validator('username')
    @classmethod
    def check_username_symbols(cls, field_value):
        '''Define allowed symbols for the username.'''
        pattern = r'[0-9A-zА-яЁё\s_-]+'
        if not re.fullmatch(pattern, field_value):
            raise ValueError(
                'Имя пользователя может содержать: '
                'кириллицу и латинские буквы, '
                'цифры и некоторые специальные символы: '
                'подчеркивание, пробел, дефис'
            )
        return field_value

    @field_validator('username')
    @classmethod
    def check_username_length(cls, field_value):
        # Check length of username
        if len(field_value) < 6:
            raise ValueError('Имя пользователя должно содержать '
                             'как минимум 6 символов')
        return field_value


class UserRead(UserBase):
    id: int
    is_active: bool
