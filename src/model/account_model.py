from uuid import UUID
from pydantic import BaseModel, Field
from typing import List

from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

class AccountModel(BaseModel):
    email: str = Field(description="メールアドレス", example="yamada@example.com")
    password: str = Field(description="パスワード", example="password")
    role_type: str = Field(description="ロールタイプ", example="admin")
    role_id: str = Field(description="ロールID", example="123e4567-e89b-12d3-a456-426614174000")
    created_at: datetime = Field(description="アカウントが作成された日時", example="2022-01-01T00:00:00+09:00")
    updated_at: datetime = Field(description="アカウントが更新された日時", example="2022-01-01T00:00:00+09:00")

class AuthModel(BaseModel):
    access_token: str = Field(description='JWTトークン')
    token_type: str = Field(description='トークンの種類')

class AccountRegisterSuccessResponse(BaseModel):
    message: str = Field(default="Account registered successfully")
    data: List[AccountModel] = Field(description="Accountの登録後のデータを返す。配列の要素は１件になる")

class AccountGetSuccessResponse(BaseModel):
    message: str = Field(default="Account get successfully")
    data: List[AccountModel] = Field(description="Account情報を取得した結果、複数のデータが返る")

class AccountUpdateSuccessResponse(BaseModel):
    message: str = Field(default="Account updated successfully")
    data: List[AccountModel] = Field(description="Accountの更新後のデータを返す。配列の要素は１件になる")

class AccountDeleteSuccessResponse(BaseModel):
    message: str = Field(examples={"info": "Account deleted successfully", "deleted_account_id": "123e4567-e89b-12d3-a456-426614174000"},
                         default={"info": "Account deleted successfully", "deleted_account_id": "123e4567-e89b-12d3-a456-426614174000"})
    data: List[AccountModel] = Field(description="Accountの情報を削除するので、配列の要素は0件になる", default=[])
class AccountPynamoModel(Model):
    class Meta:
        table_name = "account"
        aws_access_key_id = 'dummy'
        aws_secret_access_key = 'dummy'
        region = 'ap-northeast-1'
        host = "http://dynamodb-local:8000"
    id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute(null=True)
    password = UnicodeAttribute(null=True)
    role_type = UnicodeAttribute(null=True)
    role_id = UnicodeAttribute(null=True)
    created_at = UnicodeAttribute(null=True)
    updated_at = UnicodeAttribute(null=True)

def get_account_pynamo_model() -> AccountPynamoModel:
    return AccountPynamoModel

def get_account_model_from_account_pynamo_model(pynamo_model: AccountPynamoModel) -> AccountModel:
    return AccountModel(
        id=pynamo_model.id,
        email=pynamo_model.email,
        password=pynamo_model.password,
        role_type=pynamo_model.role_type,
        role_id=pynamo_model.role_id,
        created_at=pynamo_model.created_at,
        updated_at=pynamo_model.updated_at
    )