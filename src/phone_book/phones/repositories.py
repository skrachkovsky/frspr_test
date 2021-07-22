import deal
import typing

from ..database import db
from ..exceptions import ItemDoesNotExists
from .models import phones
from .aggregates import Phone

if typing.TYPE_CHECKING:
    from aiopg.sa.connection import SAConnection


@deal.pre(lambda pk: isinstance(pk, int), exception=TypeError)
@deal.pre(lambda pk: pk > 0, exception=ValueError)
@deal.post(lambda res: res is None or isinstance(res, Phone))
async def load_phone(pk: int) -> typing.Union[Phone, None]:
    async with db.engine.acquire() as conn:
        conn: 'SAConnection'
        res = await (await conn.execute(phones.select().where(phones.c.id == pk))).first()
        if not res:
            raise ItemDoesNotExists
        return Phone(**dict(res))


@deal.post(lambda res: isinstance(res, list))
async def load_phones() -> typing.List[Phone]:
    async with db.engine.acquire() as conn:
        conn: 'SAConnection'
        res = []
        cres = await conn.execute(phones.select().order_by('fullname'))
        while True:
            chunk = await cres.fetchmany(200)
            if not chunk:
                break
            res += [Phone(**dict(item)) for item in chunk]
        return res
