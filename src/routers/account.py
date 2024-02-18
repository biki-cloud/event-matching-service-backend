from typing import List
from fastapi import APIRouter, Body, Path, Query
from src.domain.account import AccountDomain, AccountModel, AuthModel
from logging import getLogger
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from src.domain.account import AccountModel
from src.repository.account import AccountRepository


logger = getLogger(__name__)

class AccountRouter:
    def __init__(self, account_domain: AccountDomain) -> None:
        self.__account_domain = account_domain

    @property
    def router(self):
        router = APIRouter(prefix='/account', tags=['Account'])

        @router.post("/register", response_model=AccountModel)
        def register_account(account: AccountModel = Body(...)):
            return self.__account_domain.register_account(account)
        
        @router.get("/all", response_model=List[AccountModel])
        def get_all_accounts():
            return self.__account_domain.get_all_accounts()

        @router.get("/get/{account_id}", response_model=AccountModel)
        def get_account(account_id: str = Path(...)):
            return self.__account_domain.get_account(account_id)

        @router.put("/edit", response_model=AccountModel)
        def update_account(account: AccountModel = Body(...)):
            return self.__account_domain.update_account(account)

        @router.delete("/delete/{account_id}", response_model=dict)
        def delete_account(account_id: str = Path(...)):
            return self.__account_domain.delete_account(account_id)
        
        @router.get("/search", response_model=List[AccountModel])
        def search_accounts(account_name: str = Query(...)):
            return self.__account_domain.search_accounts(account_name)
        
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