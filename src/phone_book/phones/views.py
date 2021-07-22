from fastapi import HTTPException

from phone_book.exceptions import ItemDoesNotExists

from .repositories import load_phone, load_phones
from .services import AddPhoneNumber, ModifyPhoneNumber, PhoneContext
from .aggregates import Phone
from . import phones_app as app


@app.get('/')
async def read_phone_book():
    return await load_phones()


@app.get('/{pk}/')
async def read_phone_number(pk: int):
    return await load_phone(pk)


@app.post('/')
async def add_new_phone_number(item: Phone):
    await AddPhoneNumber().add(PhoneContext(phone=item))
    return item


@app.put('/{pk}/')
async def edit_phone_number(pk: int, item: Phone):
    item.id = pk
    await ModifyPhoneNumber().modify(PhoneContext(phone=item))
    return item


@app.delete('/{pk}/')
async def delete_phone_number(pk: int):
    try:
        await ModifyPhoneNumber().modify(PhoneContext(phone=await load_phone(pk)))
    except ItemDoesNotExists:
        raise HTTPException(status_code=404, detail="Item not found")
