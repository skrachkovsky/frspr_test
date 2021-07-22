from functools import cached_property
import typing
import sqlalchemy
from aiopg.sa import create_engine

if typing.TYPE_CHECKING:
    from aiopg import sa

__all__ = 'db',


class Database:
    _engine: 'sa.engine.Engine'

    @cached_property
    def metadata(self):
        return sqlalchemy.MetaData()

    @property
    def engine(self) -> 'sa.engine.Engine':
        return self._engine

    async def create_engine(self) -> 'sa.engine.Engine':
        from . import conf

        try:
            self._engine.close()
        except AttributeError:
            pass
        finally:
            self._engine = await create_engine(**conf.DATABASE)
        return self._engine


db = Database()

from .models import *  # noqa
