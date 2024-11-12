from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class MainDBSettings(BaseSettings):
    '''Describes environment variables that must be provided to run main app'''
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_NAME: str
    DB_PORT: Optional[str] = '5432'
    DB_ADDRESS: Optional[str] = 'localhost'

    model_config = SettingsConfigDict(env_file=".env")


class TestingSettings(BaseSettings):
    '''
    Describes environment variables that must be provided
    to run test suite.
    '''
    TEST_DB_PASSWORD: str
    TEST_DB_USERNAME: str
    TEST_DB_NAME: str
    TEST_DB_PORT: Optional[str] = '5432'
    TEST_DB_ADDRESS: Optional[str] = 'localhost'

    model_config = SettingsConfigDict(env_file=".env.test")
