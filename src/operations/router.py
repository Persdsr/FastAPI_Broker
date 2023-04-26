import time
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from database import get_async_session

from operations.models import operation
from operations.schemas import Operation, OperationCreate

from tasks.tasks import send_email_report_dashboard

router = APIRouter(
    prefix="/operations",
    tags=['Operation']
)


@router.get('/long-operation')
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много данных, которые вычисляются сто лет"


@router.get("/", response_model=List[Operation])
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return result.all()


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
