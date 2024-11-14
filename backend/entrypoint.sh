
# Go to directory with alembic folder
cd /app/todo_tracker
# Run migration
PYTHONPATH=../${pwd} alembic upgrade head
fastapi run /app/todo_tracker/main.py --proxy-headers --host 0.0.0.0 --port 8000