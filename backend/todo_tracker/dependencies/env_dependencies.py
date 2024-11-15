from functools import lru_cache

from todo_tracker.config import MainDBSettings, TestingSettings


@lru_cache
def get_testing_settings():
    '''
    Return object with settings required for running pytest test suite.
    Function resulted hashed because TestingSettings the same for all
    testing cases
    '''
    return TestingSettings()


@lru_cache
def get_main_database_settings():
    '''
    Return object with settings required for main DB  connection.
    Function resulted hashed because MainDBSettings the same for
    the entire lifespan of the app
    '''
    return MainDBSettings()
