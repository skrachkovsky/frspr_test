import typing
from sqlalchemy import func
from pydantic.main import BaseModel
from aiopg.sa.connection import SAConnection

from phone_book.exceptions import IsNotModified, ItemDoesNotExists, ItemExists

from ..database import db
from .aggregates import Phone
from .models import phones

__all__ = 'PhoneContext', 'AddPhoneNumber', 'ModifyPhoneNumber', 'DeletePhoneNumber'


class PhoneContext(BaseModel):
    phone: Phone
    conn: typing.Optional[SAConnection]

    class Config:
        arbitrary_types_allowed = True


class AddPhoneNumber:
    async def add(self, ctx: PhoneContext):
        async with db.engine.acquire() as conn:
            ctx.conn = conn
            await self._check_exists(ctx)
            await self._add_phone(ctx)

    async def _check_exists(self, ctx: PhoneContext):
        q = phones.select().with_only_columns(func.count(phones.c.id)) \
            .where((phones.c.fullname == ctx.phone.fullname) & (phones.c.address == ctx.phone.address)
                   & (phones.c.phone == ctx.phone.phone))

        if await ctx.conn.scalar(q):
            raise ItemExists

    async def _add_phone(self, ctx: PhoneContext):
        values = ctx.phone.dict()
        if 'id' in values:
            del values['id']
        ctx.phone.id = await ctx.conn.scalar(phones.insert().values(**values))


class ModifyPhoneNumber:
    async def modify(self, ctx: PhoneContext):
        async with db.engine.acquire() as conn:
            ctx.conn = conn
            await self._check_same_exists(ctx)
            await self._save_phone(ctx)

    async def _check_same_exists(self, ctx: PhoneContext):
        q = phones.select().with_only_columns(func.count(phones.c.id)) \
            .where((phones.c.fullname == ctx.phone.fullname) & (phones.c.address == ctx.phone.address)
                   & (phones.c.phone == ctx.phone.phone) & (phones.c.id != ctx.phone.id))

        if await ctx.conn.scalar(q):
            raise ItemExists('Same item already exist')

    async def _save_phone(self, ctx: PhoneContext):
        values = ctx.phone.dict()
        if 'id' in values:
            del values['id']
        if not (await ctx.conn.execute(phones.update().where(phones.c.id == ctx.phone.id).values(**values))) \
                .rowcount:
            raise IsNotModified


class DeletePhoneNumber:
    async def delete(self, ctx: PhoneContext):
        async with db.engine.acquire() as conn:
            ctx.conn = conn
            await self._delete_phone(ctx)

    async def _delete_phone(self, ctx: PhoneContext):
        if not (await ctx.conn.execute(phones.delete().where(phones.c.id == ctx.phone.id))).rowcount:
            raise ItemDoesNotExists
