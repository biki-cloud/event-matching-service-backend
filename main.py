



import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.service.event_service import EventService
from src.repository.event_repository import EventRepository
from src.router.event_router import EventRouter

from src.service.eventer_service import EventerService
from src.repository.eventer_repository import EventerRepository
from src.router.eventer_router import EventerRouter

from src.service.account_service import AccountService
from src.repository.account_repository import AccountRepository
from src.router.account_router import AccountRouter

from src.model.account_model import get_account_pynamo_model
from src.model.event_model import get_event_pynamo_model
from src.model.eventer_model import get_eventer_pynamo_model

from src.settings.settings import get_api_description

app = FastAPI(
    title="event-matching-service",
    description=get_api_description(),
    version="0.0.1",
    summary="イベントマッチングサービスのAPI"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


event_repository = EventRepository(get_event_pynamo_model)
event_domain = EventService(event_repository)
event_router = EventRouter(event_domain)
app.include_router(event_router.router)

eventer_repository = EventerRepository(get_eventer_pynamo_model)
eventer_domain = EventerService(eventer_repository)
eventer_router = EventerRouter(eventer_domain)
app.include_router(eventer_router.router)

account_repository = AccountRepository(get_account_pynamo_model)
account_domain = AccountService(account_repository)
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
