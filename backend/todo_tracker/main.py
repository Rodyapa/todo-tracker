from fastapi import FastAPI

from todo_tracker.routers import auth

app = FastAPI()

app.include_router(auth.router)
