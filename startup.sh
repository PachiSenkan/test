#! /usr/bin/env bash

set -e
set -x

while !</dev/tcp/db/5432; 
    do sleep 1;
done;

mkdir -p app/alembic/versions

alembic revision --autogenerate
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0