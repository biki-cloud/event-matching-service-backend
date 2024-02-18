from logging import getLogger
from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi import HTTPException

from src.domain.event import EventDomain, EventModel

logger = getLogger(__name__)

class EventRouter:
    def __init__(self, event_domain: EventDomain) -> None:
        self.__event_domain = event_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/event', tags=['Event'])
        
        @api_router.get('/')
        def index_route():
            return 'Hello! Welcome to Event index route'

        @api_router.post('/register/{eventer_id}', response_model=dict)
        def register_event(event_model: EventModel = Body(...), eventer_id: str = Path(...)):
            return self.__event_domain.register_event(event_model, eventer_id)
        
        @api_router.get('/all', response_model=List[EventModel])
        def get_all():
            return self.__event_domain.get_all()

        @api_router.get('/get/{event_id}', response_model=EventModel)
        def get_event(event_id: str = Path(...)):
            try:
                return self.__event_domain.get_event(event_id)
            except KeyError:
                raise HTTPException(status_code=400, detail='No event found')
        
        @api_router.get('/get_by_eventer_id/{eventer_id}', response_model=List[EventModel])
        def get_event(eventer_id: str = Path(...)):
            try:
                return self.__event_domain.get_event_by_eventer_id(eventer_id)
            except KeyError:
                raise HTTPException(status_code=400, detail='No event found')

        @api_router.put('/update', response_model=dict)
        def update_event(event_model: EventModel):
            return self.__event_domain.update_event(event_model)

        @api_router.delete('/delete/{event_id}', response_model=dict)
        def delete_event(event_id: str):
            return self.__event_domain.delete_event(event_id)
        
        @api_router.get('/search', response_model=List[EventModel])
        def search_event(event_name: str = Query(...)):
            return self.__event_domain.search_event(event_name)

        

        return api_router
