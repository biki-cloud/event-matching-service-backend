"""
EventRouterのテスト
dynamoDBからの返答はモックを使って擬似的に作成.
主にrouter, domain層のテストを行う
router <-> service <-> repository
"""

from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from unittest.mock import patch
from src.service.event import EventService, EventModel

# テストクライアントを作成
client = TestClient(app)

@patch.object(EventService, 'register_event')
def test_register_event(mock_domain_register_event):
    id = str(uuid4())
    mock_domain_register_event.return_value = EventModel(
        event_name="Test Event",
        event_info="This is a test event",
        event_state="draft",
        id=id
    )
    
    # エントリーポイントにリクエストを送信
    response = client.post(
        "/event/register",
        json={"event_name": "Test Event", "event_info": "This is a test event", "event_state": "draft"}
    )

    # レスポンスの検証
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["event_name"] == "Test Event"
    assert data["event_info"] == "This is a test event"
    assert data["event_state"] == "draft"
    assert data["id"] == id

@patch.object(EventService, 'get_all')
def test_get_all_event(mock_domain_get_all):
    mock_domain_get_all.return_value = [
        {
            "event_name": "Test Event 1",
            "event_info": "This is a test event 1", 
            "event_state": "draft",
            "id": str(uuid4())
        },
        {
            "event_name": "Test Event 2",
            "event_info": "This is a test event 2", 
            "event_state": "open",
            "id": str(uuid4())
        }
    ]
    
    response = client.get("/event/all")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["event_name"] == "Test Event 1"
    assert data[1]["event_name"] == "Test Event 2"

@patch.object(EventService, 'update_event')
def test_update_event(mock_domain_update_event):
    id = str(uuid4())
    mock_domain_update_event.return_value = {
        "event_name": "Updated Event",
        "event_info": "This is an updated test event", 
        "event_state": "open",
        "id": id
    }
    
    response = client.put(
        f"/event/edit",
        json={
            "event_name": "Updated Event", 
            "event_info": "This is an updated test event", 
            "event_state": "open"
            }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["event_name"] == "Updated Event"
    assert data["event_info"] == "This is an updated test event"
    assert data["event_state"] == "open"
    assert data["id"] == id

@patch.object(EventService, 'delete_event')
def test_delete_event(mock_domain_delete_event):
    id = str(uuid4())
    mock_domain_delete_event.return_value = {}
    
    response = client.delete(f"/event/delete/{id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data == {}