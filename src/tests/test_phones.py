import pytest


@pytest.mark.asyncio
async def test_phones_list(client, phone):
    await phone('Test name 1', 'Test address', 375291234567)
    await phone('Test name 2', 'Test address', 375291234567)
    async with client as cn:
        resp = await cn.get('/phones/')
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_phone_detail(client, phone):
    item = await phone('Test name 3', 'Test address', 375291234567)
    async with client as cn:
        resp = await cn.get(f'/phones/{item.id}/')
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_add_phone(client):
    async with client as cn:
        resp = await cn.post('/phones/',
                             json={'fullname': 'Test name 4', 'address': 'Test address', 'phone': 375291234567})
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_change_phone(client, phone):
    item = await phone('Test name 5', 'Test address', 375291234567)
    async with client as cn:
        resp = await cn.put(f'/phones/{item.id}/',
                            json={'fullname': 'Test name 5alt', 'address': 'Test address', 'phone': 375291234567})
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_delete_phone(client, phone):
    item = await phone('Test name 6', 'Test address', 375291234567)
    async with client as cn:
        resp = await cn.delete(f'/phones/{item.id}/')
    assert resp.status_code == 200
