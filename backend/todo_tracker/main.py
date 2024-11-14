from fastapi import FastAPI
from todo_tracker.redis.redis_config import get_redis_client
from todo_tracker.routers import auth, task
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = get_redis_client()
    app.state.redis = get_redis_client()
    yield
    await redis_client.aclose()

app = FastAPI(
    title='Todo-tracker',
    lifespan=lifespan)

app.include_router(auth.router)
app.include_router(task.router)
