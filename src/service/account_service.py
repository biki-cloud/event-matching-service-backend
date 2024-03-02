from typing import List, Union
from uuid import uuid4
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
from src.model.account_model import (
    AccountDeleteSuccessResponse,
    AccountGetSuccessResponse,
    AccountModel,
    AccountRegisterSuccessResponse,
    AccountUpdateSuccessResponse,
    AuthModel
)
from src.helper.auth import (
    verify_password,
    get_password_hash,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.helper.auth import create_access_token

from src.repository.account_repository import AccountRepository

from logging import getLogger

logger = getLogger(__name__)


class AccountService:
    def __init__(self, repository: AccountRepository) -> None:
        self.repository = repository

    def register_account(self, account_data: AccountModel) -> AccountRegisterSuccessResponse:
        logger.info(account_data)
        account_data.id = str(uuid4())
        account_data.password = get_password_hash(account_data.password)

        try:
            response = self.repository.register_account(account_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")
        return AccountRegisterSuccessResponse(message="Account registered successfully", data=[response])

    def get_accounts(self, account_id: Union[str, None] = None) -> AccountGetSuccessResponse:
        try:
            if account_id:
                account_data = self.repository.get_account(account_id)
                return AccountGetSuccessResponse(message="Account get successfully", data=[account_data])
            else:
                accounts: List[AccountModel] = self.repository.get_all_accounts()
                response = AccountGetSuccessResponse(data=accounts)
                return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")

    def update_account(self, account: AccountModel) -> AccountUpdateSuccessResponse:
        try:
            updated_account_data = self.repository.update_account(account)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")

        return AccountUpdateSuccessResponse(message="Account updated successfully", data=[updated_account_data])

    def delete_account(self, account_id: str) -> AccountDeleteSuccessResponse:
        try:
            self.repository.delete_account(account_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")

        return AccountDeleteSuccessResponse(
            message={"info": "Account deleted successfully", "deleted_account_id": str(account_id)}, data=[])


    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> AccountModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        email = ""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        account = AccountModel(**self.repository.get_account_by_email(email)[0])
        if account is None:
            raise credentials_exception
        return account

    def get_access_token_for_login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        email = form_data.username
        account = AccountModel(**self.repository.get_account_by_email(email)[0])
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(form_data.password, account.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": account.email}, expires_delta=access_token_expires
        )

        return AuthModel(access_token=access_token, token_type="bearer")

    def get_me(self, email: str):
        account_data = AccountModel(**self.repository.get_account_by_email(email)[0])
        return account_data
