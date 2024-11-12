from functools import lru_cache

from todo_tracker.config import MainDBSettings, TestingSettings


@lru_cache
def get_testing_settings():
    return TestingSettings()


@lru_cache
def get_main_database_settings():
    return MainDBSettings()
