from typing import List
from fastapi import APIRouter, Body, Path, Query
from src.domain.eventer import EventerDomain, EventerModel, EventerRegisterSuccessResponse, EventerGetSuccessResponse, EventerDeleteSuccessResponse, EventerUpdateSuccessResponse
from logging import getLogger


logger = getLogger(__name__)

class EventerRouter:
    def __init__(self, eventer_domain: EventerDomain) -> None:
        self.__eventer_domain = eventer_domain

    @property
    def router(self):
        router = APIRouter(prefix='/eventer', tags=['Eventer'])

        @router.post("/register", 
                     response_model=EventerRegisterSuccessResponse
        )
        def register_eventer(eventer: EventerModel = Body(...)):
            return self.__eventer_domain.register_eventer(eventer)
        
        @router.get("/all", 
                    response_model=EventerGetSuccessResponse
        )
        def get_all_eventers():
            return self.__eventer_domain.get_all_eventers()

        @router.get("/get/{eventer_id}", 
                    response_model=EventerGetSuccessResponse
        )
        def get_eventer(eventer_id: str = Path(...)):
            return self.__eventer_domain.get_eventer(eventer_id)

        @router.put("/edit", 
                    response_model=EventerUpdateSuccessResponse
        )
        def update_eventer(eventer: EventerModel = Body(...)):
            return self.__eventer_domain.update_eventer(eventer)

        @router.delete("/delete/{eventer_id}", 
                       response_model=EventerDeleteSuccessResponse
        )
        def delete_eventer(eventer_id: str = Path(...)):
            return self.__eventer_domain.delete_eventer(eventer_id)
        
        @router.get("/search", 
                    response_model=EventerGetSuccessResponse
        )
        def search_eventers(eventer_name: str = Query(...)):
            return self.__eventer_domain.search_eventers(eventer_name)

        return router