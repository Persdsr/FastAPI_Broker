from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from config import REDIS_HOST, REDIS_PORT

from operations.router import router as router_operation
from tasks.router import router as router_tasks
from auth.base_config import fastapi_users, User

from redis import asyncio as aioredis
from pages.router import router as router_pages
from chat.router import router as router_chat

from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Trading App'
)

app.mount('/static', StaticFiles(directory='static'), name='static')

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get('protected-route')
def protected_route(user: User = Depends(current_user)):
    return f'Hello, {user.username}'


@app.get('unprotected-route')
def protected_route():
    return f'Hello, anon'


app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)

@app.get('/username')
async def get_username(user=Depends(current_user)):
    return {'status_code': 200,
            'username': user
            }

origins = [
    'http://localhost:8000',
    'http://localhost',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=["Access-Control-Allow-Origin", "Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"]
)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


def get_dep_test(limit: int, skip: int):
    return {'limit': limit, 'skip': skip}

@app.get('/test_depends/', dependencies=[Depends(get_dep_test)])
async def get_test_dep():
    return {'status_code': 200}


app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)