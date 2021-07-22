import typing
import pytest
import asyncio
import os
from httpx import AsyncClient
from aiopg.sa import create_engine
from alembic import command
from alembic.config import Config

from phone_book import app, conf
from phone_book.database import db
from phone_book.phones.aggregates import Phone
from phone_book.settings import ROOT_DIR
from phone_book.models import phones

if typing.TYPE_CHECKING:
    from aiopg.sa.connection import SAConnection


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def setup_database():
    engine = await create_engine(**conf.DATABASE)
    new_database = 'test_' + conf.DATABASE['database']
    async with engine.acquire() as conn:
        conn: 'SAConnection'
        await conn.execute(f'DROP DATABASE IF EXISTS {new_database}')
        await conn.execute(f'CREATE DATABASE {new_database}')
        await conn.execute(f'GRANT ALL PRIVILEGES ON DATABASE {new_database} TO "{conf.DATABASE["user"]}"')
    conf.DATABASE['database'] = new_database
    alembic_cfg = Config(os.path.join(ROOT_DIR, 'migrations', 'alembic_test.ini'))
    command.upgrade(alembic_cfg, 'head')


@pytest.fixture(scope='session')
async def database_connection():
    return await db.create_engine()


@pytest.fixture(scope='session')
async def conn(setup_database, database_connection):
    async with database_connection.acquire() as conn:
        yield conn


@pytest.fixture(scope='session')
async def client():
    yield AsyncClient(app=app, base_url='http://test')


@pytest.fixture
async def phone(conn):
    async def create_phone(fullname, address, phone_number):
        item = Phone(fullname=fullname, address=address, phone=phone_number)
        values = item.dict()
        if 'id' in values:
            del values['id']
        item.id = await conn.scalar(phones.insert().values(**values))
        return item
    yield create_phone
