from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class MainDBSettings(BaseSettings):
    '''Describes environment variables that must be provided to run main app'''
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_NAME: str
    DB_PORT: Optional[str] = '5432'
    DB_HOST: Optional[str] = 'localhost'

    # model_config = SettingsConfigDict(env_file=".env",
    #                                  extra='allow')


class TestingSettings(BaseSettings):
    '''
    Describes environment variables that must be provided
    to run test suite.
    '''
    TEST_DB_PASSWORD: str
    TEST_DB_USERNAME: str
    TEST_DB_NAME: str
    TEST_DB_PORT: Optional[str] = '5432'
    TEST_DB_HOST: Optional[str] = 'localhost'

    model_config = SettingsConfigDict(env_file=".env",
                                      extra='allow')


class JWTSettings(BaseSettings):
    '''
    Describes data used for JWT Token Authnetication
    '''
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: Optional[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 15
    REFRESH_TOKEN_EXPIRE_DAYS: Optional[int] = 1

    # model_config = SettingsConfigDict(env_file=".env",
    #                                   extra='allow')


class RedisSettings(BaseSettings):
    '''
    Describes data used for Redis connection
    '''
    REDIS_HOST: Optional[str] = 'localhost'
    REDIS_PORT: Optional[int] = 6379
