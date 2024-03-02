from pydantic import BaseModel, Field
from typing import List
from src.model.event_model import EventModel

class EventModel(BaseModel):
    id: Union[UUID, None] = Field(default=None, description="イベントID", example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(description="イベント名", example="祭り")
    state: str = Field(description="イベント状態", example="draft or open or close")
    info: str = Field(description="イベント情報", example="祭りの説明")
    eventer_id: Union[UUID, None] = Field(default=None, description="イベントID", example="123e4567-e89b-12d3-a456-426614174000")

class EventRegisterSuccessResponse(BaseModel):
    message: str = Field(default="Event registered successfully")
    data: List[EventModel] = Field(description="Eventの登録後のデータを返す。配列の要素は１件になる")

class EventGetSuccessResponse(BaseModel):
    message: str = Field(default="Event get successfully")
    data: List[EventModel] = Field(description="Event情報を取得した結果、複数のデータが返る")

class EventUpdateSuccessResponse(BaseModel):
    message: str = Field(default="Event updated successfully")
    data: List[EventModel] = Field(description="Eventの更新後のデータを返す。配列の要素は１件になる")

class EventDeleteSuccessResponse(BaseModel):
    message: str = Field(default="Event deleted successfully")
    data: List[EventModel] = Field(description="Eventの情報を削除するので、配列の要素は0件になる", default=[])

class EventPynamoModel(Model):
    class Meta:
        table_name = "event"
        aws_access_key_id = 'dummy'        
        aws_secret_access_key = 'dummy'
        region = 'ap-northeast-1'
        host = "http://dynamodb-local:8000"
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=True)
    state = UnicodeAttribute(null=True)
    info = UnicodeAttribute(null=True)
    eventer_id = UnicodeAttribute(null=True)

def get_event_pynamo_model() -> EventPynamoModel:
    return EventPynamoModel

def get_event_model_from_event_pynamo_model(pynamo_model: EventPynamoModel) -> EventModel:
    return EventModel(
        id=pynamo_model.id,
        name=pynamo_model.name,
        state=pynamo_model.state,
        info=pynamo_model.info,
        eventer_id=pynamo_model.eventer_id
    )
