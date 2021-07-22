from fastapi import FastAPI

__all__ = 'phones_app',

phones_app = FastAPI()

from . import views  # noqa
