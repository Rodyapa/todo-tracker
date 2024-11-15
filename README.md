# todo-tracker
## Просмотр проекта на локальной машине:
Склонировать репозиторий на локальную машину:
```
git clone git@github.com:Rodyapa/todo-tracker.git
```
Перейти в директорию infra
```
cd todo-tracker/infra
```
Создать .env файл с конфигурацией проекта
```
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=local_dev
POSTGRES_DB=todo_tracker

DB_PASSWORD=local_dev
DB_USERNAME=todo_user
DB_NAME=todo_tracker
DB_HOST=db

JWT_SECRET_KEY=cee5805303871f76fd43850525453913f7aa711d1a69834e43431dc4f470775e
JWT_REFRESH_SECRET_KEY=d9a02d3f903a2266a5fcbeeeacb176f04088672841ab7c15a36264dbd5b7fa01

TEST_DB_PASSWORD=local_dev
TEST_DB_USERNAME=todo_user
TEST_DB_NAME=todo_tracker_test

AIOHTTP_HOST=0.0.0.0
AIOHTTP_PORT=8080

REDIS_HOST=redis

```
Собрать и запустить контейнеры локально
```
sudo docker compose -f docker-compose.yml up --build
```
## Endpoints
* 0.0.0.0:8080/docs/ - Документация эндпоинтов.

## Технологии:
    *Python
    *FastAPI
    *AIOHTTP
    *Poetry
    *pytest library 
