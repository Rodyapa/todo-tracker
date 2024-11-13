from fastapi import FastAPI

from todo_tracker.routers import auth, task

app = FastAPI()

app.include_router(auth.router)
app.include_router(task.router)
