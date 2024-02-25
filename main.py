

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from src.models.eventer import get_eventer_pynamo_model
from src.internal.db import initialize_db

from src.domain.event import EventDomain
from src.repository.event import EventRepository
from src.routers.event import EventRouter

from src.domain.eventer import EventerDomain
from src.repository.eventer import EventerRepository
from src.routers.eventer import EventerRouter

from src.domain.account import AccountDomain
from src.repository.account import AccountRepository
from src.routers.account import AccountRouter

from src.settings.settings import get_api_description


app = FastAPI(
    title="event-matching-service",
    description=get_api_description(),
    version="0.0.1", 
    summary="イベントマッチングサービスのAPI"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

db = initialize_db()


event_repository = EventRepository(db, 'event')
event_domain = EventDomain(event_repository)
event_router = EventRouter(event_domain)
app.include_router(event_router.router)

eventer_repository = EventerRepository(get_eventer_pynamo_model)
eventer_domain = EventerDomain(eventer_repository)
eventer_router = EventerRouter(eventer_domain)
app.include_router(eventer_router.router)

account_repository = AccountRepository(db, 'account')
account_domain = AccountDomain(account_repository, eventer_repository)
account_router = AccountRouter(account_domain)
app.include_router(account_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: 本番環境では許可するドメインを指定する
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    # 基本的には各ルーターの中で例外を発生させ、返すので、ここには来ないが、漏れたものだけここにくる
    # 漏れたものは全て以下の内容でレスポンスを返す
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

@app.get("/hello")
def hello():
    return {"hello": "world"}