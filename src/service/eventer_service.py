
from typing import List, Union
from uuid import UUID, uuid4
from fastapi import HTTPException

from pydantic import BaseModel, Field
from src.model.eventer_model import EventerModel, EventerPynamoModel
from src.model.eventer_model import EventerGetSuccessResponse, EventerRegisterSuccessResponse, EventerUpdateSuccessResponse, EventerDeleteSuccessResponse
from src.repository.eventer_repository import EventerRepository


class EventerService:
    def __init__(self, repository: EventerRepository) -> None:
        self.repository = repository

    def register_eventer(self, eventer_data: EventerModel) -> EventerRegisterSuccessResponse:
        if eventer_data.account_id is None:
            raise HTTPException(status_code=400, detail="account_id is required")

        eventer_data.id = str(uuid4())
        eventer_data.account_id = str(eventer_data.account_id)

        res: EventerModel = self.repository.register_eventer(eventer_data)

        response = EventerRegisterSuccessResponse(
            data=[res]
        )
        return response

    def get_eventer(self, eventer_id: int = None) -> EventerGetSuccessResponse:
        db_res: EventerModel = self.repository.get_eventer(eventer_id)
        response = EventerGetSuccessResponse(data=[db_res])
        return response

    def update_eventer(self, eventer_data: EventerModel) -> EventerUpdateSuccessResponse:
        try:
            db_res = self.repository.update_eventer(eventer_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        response = EventerUpdateSuccessResponse(data=[db_res])
        return response

    def delete_eventer(self, eventer_id: int) -> EventerDeleteSuccessResponse:
        try:
            self.repository.delete_eventer(eventer_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        response = EventerDeleteSuccessResponse()
        response.data = []
        return response
    

    def get_all_eventers(self) -> EventerGetSuccessResponse:
        eventers: List[EventerModel] = self.repository.get_all_eventers()
        response = EventerGetSuccessResponse(data=eventers)
        return response
    
    def search_eventers(self, eventer_name: str) -> EventerGetSuccessResponse:
        eventers: List[EventerModel] = self.repository.search_eventers(eventer_name)
        response = EventerGetSuccessResponse(data=eventers)
        return response

