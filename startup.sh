#! /usr/bin/env bash

set -e
set -x

while !</dev/tcp/db/5432; 
    do sleep 1;
done;

# Run migrations
alembic revision --autogenerate
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0
# Create initial data in DB
#python app/initial_data.py