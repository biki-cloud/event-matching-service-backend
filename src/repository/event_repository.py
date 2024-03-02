from typing import Callable, List
from pynamodb.exceptions import DoesNotExist
from src.model.event_model import EventModel, EventPynamoModel, get_event_model_from_event_pynamo_model

class EventRepository:
    def __init__(self, model_get_func: Callable) -> None:
        self.__model = model_get_func()

    def get_all_events(self) -> List[EventModel]:
        try:
            pynamodb_events = list(self.__model.scan())
        except DoesNotExist:
            return []
        
        events = []
        for pynamodb_event in pynamodb_events:
            res = get_event_model_from_event_pynamo_model(pynamodb_event)
            events.append(res)
        
        return events

    def get_event(self, id: str) -> EventModel:
        try:
            event = self.__model.get(hash_key=id)
            res = get_event_model_from_event_pynamo_model(event)
            return res
        except DoesNotExist:
            raise ValueError(f"Event with id '{id}' not found")

    def register_event(self, event: EventModel) -> EventModel:
        new_event = EventPynamoModel(
            id=event.id,
            name=event.name,
            state=event.state,
            info=event.info,
            eventer_id=event.eventer_id
        )
        new_event.save()
        return event

    def update_event(self, event: EventModel) -> EventModel:
        try:
            event_item = self.__model.get(hash_key=str(event.id))
            event_item.update(actions=[
                self.__model.name.set(event.name),
                self.__model.state.set(event.state),
                self.__model.info.set(event.info),
                self.__model.eventer_id.set(str(event.eventer_id))
            ])
            return get_event_model_from_event_pynamo_model(event_item)
        except DoesNotExist:
            raise ValueError(f"Event with id {event.id} does not exist")

    def delete_event(self, id: str) -> bool:
        try:
            event = self.__model.get(hash_key=id)
            event.delete()
            return True
        except DoesNotExist:
            raise ValueError(f"Event with id {id} does not exist")
