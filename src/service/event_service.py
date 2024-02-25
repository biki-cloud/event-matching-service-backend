from uuid import uuid4
from pydantic import Field
from decimal import Decimal
from pydantic import BaseModel
from pydantic.types import UUID4
from typing import List, Optional, Union
from uuid import UUID, uuid4

from src.repository.event_repository import EventRepository
from src.model.event_model import EventModel, EventRegisterSuccessResponse, EventGetSuccessResponse, EventUpdateSuccessResponse, EventDeleteSuccessResponse


class EventService():
    def __init__(self, repository: EventRepository) -> None:
        self.__repository = repository

    def get_all(self) -> EventGetSuccessResponse:
        events = self.__repository.get_all_events()
        return EventGetSuccessResponse(data=[events])

    def get_event(self, id: str) -> EventGetSuccessResponse:
        event = self.__repository.get_event(id)
        return EventGetSuccessResponse(data=[event])
    
    def get_event_by_eventer_id(self, eventer_id: str) -> EventGetSuccessResponse:
        events = self.__repository(eventer_id)
        return EventGetSuccessResponse(data=events)

    def register_event(self, event: EventModel, eventer_id: str) -> EventRegisterSuccessResponse:
        event.id = str(uuid4())
        event.eventer_id = eventer_id.replace('"', '')
        res = self.__repository.register_event(event.dict())
        if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
            raise ValueError(res)
        print(event.dict())
        return EventRegisterSuccessResponse(data=[event])

    def update_event(self, event: EventModel) -> EventUpdateSuccessResponse:
        print(event.dict())
        res = self.__repository.update_event(event.dict())
        if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
            raise ValueError(res)
        return EventUpdateSuccessResponse(data=[event])

    def delete_event(self, id: str) -> EventDeleteSuccessResponse:
        self.__repository.delete_event(id)
        return EventDeleteSuccessResponse(data=[])
    
    def search_event(self, event_name: str) -> List[EventModel]:
        events = self.__repository.search_event(event_name)
        return [EventModel(**event) for event in events]