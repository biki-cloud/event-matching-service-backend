import pytest
from unittest.mock import MagicMock
from src.service.event_service import EventService, EventModel
from src.repository.event_repository import EventRepository
from uuid import uuid4

@pytest.fixture
def event_repository():
    return MagicMock(spec=EventRepository)

@pytest.fixture
def event_domain(event_repository):
    return EventService(repository=event_repository)

def test_get_all(event_domain, event_repository):
    uuid1 = str(uuid4())
    uuid2 = str(uuid4())
    event_repository.get_all.return_value = [
        {
            "id": uuid1,
            "event_name": "Test Event 1",
            "event_info": "This is a test event 1",
            "event_state": "draft"
        },
        {
            "id": uuid2,
            "event_name": "Test Event 2",
            "event_info": "This is a test event 2",
            "event_state": "open"
        }
    ]
    events = event_domain.get_all()
    assert len(events) == 2
    assert all(isinstance(event, EventModel) for event in events)
    assert events[0].event_name == "Test Event 1"
    assert events[1].event_name == "Test Event 2"
    assert str(events[0].id) == uuid1
    assert str(events[1].id) == uuid2

def test_register_event(event_domain, event_repository):
    uuid = str(uuid4())
    event_data = {
        "id": uuid,
        "event_name": "New Event",
        "event_info": "This is a new event",
        "event_state": "draft"
    }
    event_repository.register_event.return_value = event_data
    event = event_domain.register_event(EventModel(**event_data))
    assert isinstance(event, EventModel)
    assert event.event_name == "New Event"
    assert event.event_info == "This is a new event"
    assert event.event_state == "draft"
    assert str(event.id) == uuid

def test_update_event(event_domain, event_repository):
    uuid = str(uuid4())
    event_data = {
        "id": uuid,
        "event_name": "Updated Event",
        "event_info": "This is an updated event",
        "event_state": "open"
    }
    event_repository.update_event.return_value = event_data
    event = event_domain.update_event(EventModel(**event_data))
    assert isinstance(event, EventModel)
    assert str(event.id) == uuid
    assert event.event_name == "Updated Event"
    assert event.event_info == "This is an updated event"
    assert event.event_state == "open"

def test_delete_event(event_domain, event_repository):
    event_id = str(uuid4())
    event_repository.delete_event.return_value = {}
    result = event_domain.delete_event(event_id)
    assert result == {}
    event_repository.delete_event.assert_called_once_with(event_id)

def test_get_event(event_domain, event_repository):
    uuid = str(uuid4())
    event_repository.get_event.return_value = {
        "id": uuid,
        "event_name": "Test Event",
        "event_info": "This is a test event",
        "event_state": "draft"
    }
    event = event_domain.get_event("1")
    assert str(event.id) == uuid
    assert event.event_name == "Test Event"
    assert event.event_info == "This is a test event"
    assert event.event_state == "draft"

def test_search_event(event_domain, event_repository):
    uuid1 = str(uuid4())
    uuid2 = str(uuid4())
    event_repository.search_event.return_value = [
        {
            "id": uuid1,
            "event_name": "Test Event 1",
            "event_info": "This is a test event 1",
            "event_state": "draft"
        },
        {
            "id": uuid2,
            "event_name": "Test Event 2",
            "event_info": "This is a test event 2",
            "event_state": "open"
        }
    ]
    events = event_domain.search_event("Test")
    assert len(events) == 2
    assert events[0].event_name == "Test Event 1"
    assert events[1].event_name == "Test Event 2"
    assert str(events[0].id) == uuid1
    assert str(events[1].id) == uuid2
