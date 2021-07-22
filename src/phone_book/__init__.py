import os
import typing
import logging.config

from fastapi import FastAPI

from .utils import load_module
from .phones import phones_app
from .database import db

if typing.TYPE_CHECKING:
    from . import settings

__all__ = 'conf', 'app'

conf: 'settings' = load_module(os.environ.get('APP_SETTINGS') or 'phone_book.settings')

logging.config.dictConfig(conf.LOGGING)

app = FastAPI()
app.mount('/phones', phones_app)


@app.on_event('startup')
async def startup_event():
    await db.create_engine()
