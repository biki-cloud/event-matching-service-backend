from uuid import uuid4
from pydantic import Field
from decimal import Decimal
from pydantic import BaseModel
from pydantic.types import UUID4
from typing import List, Optional, Union
from uuid import UUID, uuid4

from src.repository.event import EventRepository


class EventModel(BaseModel):
    id: Union[UUID, None] = Field(default=None, description="イベントID", example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(description="イベント名", example="祭り")
    state: str = Field(description="イベント状態", example="draft or open or close")
    info: str = Field(description="イベント情報", example="祭りの説明")
    eventer_id: Union[UUID, None] = Field(default=None, description="イベントID", example="123e4567-e89b-12d3-a456-426614174000")


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.__repository = repository

    def get_all(self) -> List[EventModel]:
        events = self.__repository.get_all()
        return [EventModel(**event) for event in events]

    def get_event(self, id: UUID) -> EventModel:
        return EventModel(**self.__repository.get_event(id))
    
    def get_event_by_eventer_id(self, eventer_id: str) -> List[EventModel]:
        events = self.__repository.get_event_by_eventer_id(eventer_id)
        return [EventModel(**event) for event in events]

    def register_event(self, event: EventModel, eventer_id: str) -> dict:
        event.id = str(uuid4())
        event.eventer_id = eventer_id.replace('"', '')
        res = self.__repository.register_event(event.dict())
        if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
            raise ValueError(res)
        print(event.dict())
        return {"message": "Event registered successfully", "event": EventModel(**event.dict())}

    def update_event(self, event: EventModel) -> dict:
        print(event.dict())
        res = self.__repository.update_event(event.dict())
        if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
            raise ValueError(res)
        return {"message": "Event updated successfully", "event": EventModel(**event.dict())}

    def delete_event(self, id: str) -> dict:
        return self.__repository.delete_event(id)
    
    def search_event(self, event_name: str) -> List[EventModel]:
        events = self.__repository.search_event(event_name)
        return [EventModel(**event) for event in events]