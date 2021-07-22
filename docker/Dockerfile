FROM python:3.9-alpine

ARG debug

RUN apk add --update alpine-sdk cmake make gcc libtool ca-certificates openssh-client openssl-dev postgresql-dev
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -


ENV PATH="${PATH}:/root/.poetry/bin"
COPY ./pyproject.toml /root/
COPY ./poetry.lock /root/
COPY ./migrations/alembic.ini /root/
WORKDIR /root/

RUN poetry run pip install --upgrade pip setuptools wheel setuptools_rust
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN if [ $debug = 1 ]; then poetry install ; else poetry install --no-dev ; fi && poetry cache clear pypi --all -n

ENV PYTHONPATH="$PYTHONPATH:/app/src"