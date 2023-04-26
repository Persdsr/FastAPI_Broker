from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post('/operations', json={
            "id": 2,
            "quantity": "string",
            "figi": "string",
            "instrument_type": "string",
            "date": "2023-04-14T20:09:20.577",
            "type": "string"
})

    assert response.status_code == 200