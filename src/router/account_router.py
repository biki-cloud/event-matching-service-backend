from typing import List
from fastapi import APIRouter, Body, Path, Query
from src.service.account_service import AccountService
from logging import getLogger
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.model.account_model import (
    AccountModel,
    AuthModel,
    AccountRegisterSuccessResponse,
    AccountGetSuccessResponse,
    AccountUpdateSuccessResponse,
    AccountDeleteSuccessResponse
)

logger = getLogger(__name__)


class AccountRouter:
    def __init__(self, account_domain: AccountService) -> None:
        self.__account_domain = account_domain

    @property
    def router(self):
        router = APIRouter(prefix='/account', tags=['Account'])

        @router.post("/register", response_model=AccountRegisterSuccessResponse)
        def register_account(account: AccountModel = Body(...)):
            return self.__account_domain.register_account(account)

        @router.get("/get", response_model=AccountGetSuccessResponse)
        def get_accounts(account_id: str = Query(...)):
            return self.__account_domain.get_accounts(account_id)

        @router.put("/edit", response_model=AccountUpdateSuccessResponse)
        def update_account(account: AccountModel = Body(...)):
            return self.__account_domain.update_account(account)

        @router.delete("/delete/{account_id}", response_model=AccountDeleteSuccessResponse)
        def delete_account(account_id: str = Path(...)):
            return self.__account_domain.delete_account(account_id)

        @router.post("/auth/token", response_model=AuthModel)
        async def get_access_token_for_login(form_data: OAuth2PasswordRequestForm = Depends()):
            """
            クライアントがユーザ名(email)とパスワードを使用して、DBを確認し、ユーザが存在していればこちらがトークンを返すエンドポイントです。
            OAuth2PasswordRequestFormを使用して、クライアントから送信されたユーザー名とパスワードを取得します。
            """
            return self.__account_domain.get_access_token_for_login(form_data)

        @router.get("/get_me", response_model=AccountModel)
        async def read_users_me(current_user: AccountModel = Depends(self.__account_domain.get_current_user)):
            """
            トークンで認証することが前提のエントリーポイント
            """
            return self.__account_domain.get_me(current_user.email)

        return router
