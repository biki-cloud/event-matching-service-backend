from logging import getLogger
from fastapi import APIRouter, Body, Path, Query
from fastapi import HTTPException

from src.service.event_service import EventService, EventModel, EventRegisterSuccessResponse, EventGetSuccessResponse, \
    EventUpdateSuccessResponse, EventDeleteSuccessResponse

logger = getLogger(__name__)


class EventRouter:
    def __init__(self, event_domain: EventService) -> None:
        self.__event_domain = event_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/event', tags=['Event'])

        @api_router.post('/register', response_model=EventRegisterSuccessResponse)
        def register_event(event_model: EventModel = Body(...)):
            return self.__event_domain.register_event(event_model)

        @api_router.get('/get', response_model=EventGetSuccessResponse)
        def get_events(event_id: str = Query(...),
                       eventer_id: str = Query(...),
                       event_name: str = Query(...)):
            return self.__event_domain.get_events(event_id, eventer_id, event_name)

        @api_router.put('/update', response_model=EventUpdateSuccessResponse)
        def update_event(event_model: EventModel):
            return self.__event_domain.update_event(event_model)

        @api_router.delete('/delete/{event_id}', response_model=EventDeleteSuccessResponse)
        def delete_event(event_id: str):
            return self.__event_domain.delete_event(event_id)

        return api_router
