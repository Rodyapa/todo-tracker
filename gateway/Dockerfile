# Dockerfile for aiohttp proxy
FROM python:3.12-slim

WORKDIR /app
COPY aiohttp_server_config.py .

RUN pip install aiohttp

CMD ["python", "aiohttp_server_config.py"]