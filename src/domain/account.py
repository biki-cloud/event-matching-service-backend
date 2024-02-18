
import os
from typing import List, Optional, Union
from uuid import UUID, uuid4
from fastapi import Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta
from jose import JWTError, jwt
from src.helper.auth import verify_password, get_password_hash, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.helper.auth import create_access_token

from pydantic import BaseModel, Field
from src.repository.account import AccountRepository
from src.domain.eventer import EventerModel, EventerDomain
from src.repository.eventer import EventerRepository

from logging import getLogger

logger = getLogger(__name__)


class AccountModel(BaseModel):
    id: Union[UUID, None] = Field(default=None, description="アカウントID", example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(description="名前", example="太郎")
    email: str = Field(description="メールアドレス", example="yamada@example.com")
    password: str = Field(description="パスワード", example="password")
    eventer: Optional[EventerModel] = Field(description="イベンターとして登録されていれば情報が入る", default={})

"""
AuthModelは、アクセストークンを返すエンドポイントで使用されるモデルです。
"""
class AuthModel(BaseModel):
    access_token: str = Field(description='JWTトークン')
    token_type: str = Field(description='トークンの種類')

class AccountDomain:
    def __init__(self, repository: AccountRepository, eventer_repository: EventerRepository) -> None:
        self.repository = repository
        self.__eventer_domain = EventerDomain(eventer_repository)

    def register_account(self, account_data: AccountModel) -> AccountModel:
        logger.info(account_data)
        account_data.id = str(uuid4())
        account_data.password = get_password_hash(account_data.password)

        # eventerとvendorを新規登録
        eventer = EventerModel(info="初めてのイベント")
        self.__eventer_domain.register_eventer(eventer_data=eventer, account_id=account_data.id)
        account_data.eventer = eventer

        # TODO: ハンドリングする必要がある
        response = self.repository.register_account(account_data.dict())
        return AccountModel(**self.repository.get_account(account_data.id))

    def get_account(self, account_id: int = None) -> List[AccountModel]:
        return AccountModel(**self.repository.get_account(account_id))

    def update_account(self, account_data: dict) -> AccountModel:
        return AccountModel(**self.repository.update_account(account_data))

    def delete_account(self, account_id: int) -> dict:
        return self.repository.delete_account(account_id)
    
    def get_all_accounts(self) -> List[AccountModel]:
        return [AccountModel(**account) for account in self.repository.get_all_accounts()]
    
    def search_accounts(self, account_name: str) -> List[AccountModel]:
        return [AccountModel(**account) for account in self.repository.search_accounts(account_name)]
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> AccountModel:
        """
        与えられたJWT（JSON Web Token）アクセストークンを解析して、トークンに基づいて現在のユーザー情報を取得するために使用されます。
        token: str = Depends(oauth2_scheme)でリクエストから自動的にトークンを取得する。
        """
        # 認証エラーが起きた時の例外処理
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        email = ""
        try:
            # トークンをデコードして内容を取得
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # トークンを作成する際にセットした内容からユーザー名を取得
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # DBからユーザー情報を取得
        account = AccountModel(**self.repository.get_account_by_email(email)[0])
        if account is None:
            raise credentials_exception
        return account
    
    def get_access_token_for_login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        """
        クライアントがユーザ名とパスワードを使用して、DBを確認し、ユーザが存在していればこちらがトークンを返すエンドポイントです。
        OAuth2PasswordRequestFormを使用して、クライアントから送信されたユーザー名とパスワードを取得します。
        """
        # DBにユーザーが存在するか確認
        email = form_data.username # ユーザ名はemail. ほんとはusernameとかにしたいけど、FastAPIのOAuth2PasswordRequestFormがusernameとpasswordを要求するので、ここではusernameとしている
        account = AccountModel(**self.repository.get_account_by_email(email)[0])
        # DBになかったら認証エラーを返す
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # パスワードが一致しなかったら認証エラーを返す
        if not verify_password(form_data.password, account.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # トークンを生成. トークンにユーザー名、有効期限を設定
        access_token = create_access_token(
            data={"sub": account.email}, expires_delta=access_token_expires
        )

        # 認証できたのでアクセストークンを返す
        return AuthModel(access_token=access_token, token_type="bearer")
    
    def get_me(self,email: str):
        """
        トークンで認証することが前提のエントリーポイント
        """
        return AccountModel(**self.repository.get_account_by_email(email)[0])

