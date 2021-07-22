# Test service

## Deployment

* `cd docker`
* `docker-compose up -d`

## DB init

* `docker-compose exec core bash`
* `poetry run alembic upgrade head`

## Tests

* `docker-compose exec core bash`
* `poetry run pytest /app/src/tests --rootdir=/app -vs`
