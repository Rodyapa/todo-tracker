from dotenv import load_dotenv
from redis.asyncio import Redis

from todo_tracker.config import RedisSettings

load_dotenv()

redis_settings = RedisSettings()


# Initialize Redis client
def get_redis_client() -> Redis:
    '''Get Redis client.'''
    redis_client = Redis(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        decode_responses=True
    )
    return redis_client
