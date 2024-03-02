from typing import Union
from uuid import uuid4

from fastapi import HTTPException

from src.repository.event_repository import EventRepository
from src.model.event_model import (
    EventModel,
    EventRegisterSuccessResponse,
    EventGetSuccessResponse,
    EventUpdateSuccessResponse,
    EventDeleteSuccessResponse
)


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.__repository = repository

    def get_events(self, event_id: Union[str, None] = None,
                   eventer_id: Union[str, None] = None,
                   eventer_name: Union[str, None] = None) -> EventGetSuccessResponse:
        events = []
        try:
            if event_id:
                event = self.__repository.get_event(event_id)
                events.append(event)
            elif eventer_id:
                event = self.__repository.get_event_by_eventer_id(eventer_id)
                events.append(event)
            elif eventer_name:
                events = self.__repository.search_event(eventer_name)
            else:
                events = self.__repository.get_all_events()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")
        return events

    def register_event(self, event: EventModel) -> EventRegisterSuccessResponse:
        event.id = str(uuid4())
        event.eventer_id = str(event.eventer_id).replace('"', '')
        try:
            res = self.__repository.register_event(event)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")
        return EventRegisterSuccessResponse(data=[event])

    def update_event(self, event: EventModel) -> EventUpdateSuccessResponse:
        try:
            res = self.__repository.update_event(event)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")
        return EventUpdateSuccessResponse(data=[event])

    def delete_event(self, id: str) -> EventDeleteSuccessResponse:
        try:
            self.__repository.delete_event(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error occurred: {str(e)}")

        return EventDeleteSuccessResponse(data=[])