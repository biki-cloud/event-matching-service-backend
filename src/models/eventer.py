from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute
from pynamodb.exceptions import DoesNotExist
from pydantic import BaseModel, Field
from typing import List, Union
from uuid import UUID

class EventerModel(BaseModel):
    id: Union[UUID, None] = Field(default=None, description="イベンターID", example="123e4567-e89b-12d3-a456-426614174000")
    info: Union[str, None] = Field(description="イベント主催者情報", example="祭りの説明")
    account_id: Union[UUID, None] = Field(default=None, description="イベンターが紐付いているユーザーID", example="123e4567-e89b-12d3-a456-426614174000")

class EventerGetSuccessResponse(BaseModel):
    message: str = Field(default="eventer get successfully")
    data: List[EventerModel] = Field(description="Eventer情報を取得した結果、複数のデータが返る")

class EventerRegisterSuccessResponse(BaseModel):
    message: str = Field(default="Eventer registered successfully")
    data: List[EventerModel] = Field(description="Eventerの登録後のデータを返す。配列の要素は１件になる")

class EventerUpdateSuccessResponse(BaseModel):
    message: str = Field(default="Eventer updated successfully")
    data: List[EventerModel] = Field(description="Eventerの更新後のデータを返す。配列の要素は１件になる")

class EventerDeleteSuccessResponse(BaseModel):
    message: str = Field(examples={"info": "Eventer deleted successfully", "deleted_eventer_id": "123e4567-e89b-12d3-a456-426614174000"},
                         default={"info": "Eventer deleted successfully", "deleted_eventer_id": "123e4567-e89b-12d3-a456-426614174000"})
    data: List[EventerModel] = Field(description="Eventerの情報を削除するので、配列の要素は0件になる", default=[])

class EventerPynamoModel(Model):
    class Meta:
        table_name = "eventer"
        aws_access_key_id = 'dummy'
        aws_secret_access_key = 'dummy'
        region = 'ap-northeast-1'
        host = "http://dynamodb-local:8000"
    id = UnicodeAttribute(hash_key=True)
    info = UnicodeAttribute(null=True)
    account_id = UnicodeAttribute(null=True)

def get_eventer_pynamo_model() -> EventerPynamoModel:
    return EventerPynamoModel

def get_eventer_model_from_eventer_pynamo_model(pynamo_model: EventerPynamoModel) -> EventerModel:
    return EventerModel(
        id=pynamo_model.id,
        info=pynamo_model.info,
        account_id=pynamo_model.account_id
    )

