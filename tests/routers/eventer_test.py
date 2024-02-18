"""
EventerRouterのテ
"""
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from unittest.mock import patch
from src.repository.eventer import EventerRepository

# テストクライアントを作成
client = TestClient(app)

# DBのモックを作成(DBから取得するデータを擬似的に作成)
@patch.object(EventerRepository, 'register_eventer')
def test_register_eventer(mock_register_eventer):
    id = str(uuid4())
    mock_register_eventer.return_value = {
        "eventer_name": "Test Eventer",
        "eventer_info": "This is a test eventer", 
        "id": id
        }
    
    # エントリーポイントにリクエストを送信
    response = client.post(
        "/eventer/register",
        json={"eventer_name": "Test Eventer", "eventer_info": "This is a test eventer"}
    )

    # レスポンスの検証
    assert response.status_code == 200
    data = response.json()
    assert data["eventer_name"] == "Test Eventer"
    assert data["eventer_info"] == "This is a test eventer"
    assert data["id"] == id

@patch.object(EventerRepository, 'get_all_eventers')
def test_get_all_eventers(mock_get_all_eventers):
    mock_get_all_eventers.return_value = [
        {
            "eventer_name": "Test Eventer 1",
            "eventer_info": "This is a test eventer 1", 
            "id": str(uuid4())
        },
        {
            "eventer_name": "Test Eventer 2",
            "eventer_info": "This is a test eventer 2", 
            "id": str(uuid4())
        }
    ]
    
    response = client.get("/eventer/all")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["eventer_name"] == "Test Eventer 1"
    assert data[1]["eventer_name"] == "Test Eventer 2"

@patch.object(EventerRepository, 'get_eventer')
def test_get_eventer(mock_get_eventer):
    id = str(uuid4())
    mock_get_eventer.return_value = {
        "eventer_name": "Specific Eventer",
        "eventer_info": "This is a specific eventer",
        "id": id
    }
    
    response = client.get(f"/eventer/get/{id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["eventer_name"] == "Specific Eventer"
    assert data["eventer_info"] == "This is a specific eventer"
    assert data["id"] == id

@patch.object(EventerRepository, 'update_eventer')
def test_update_eventer(mock_update_eventer):
    id = str(uuid4())
    mock_update_eventer.return_value = {
        "eventer_name": "Updated Eventer",
        "eventer_info": "This is an updated eventer",
        "id": id
    }
    
    response = client.put(
        f"/eventer/edit",
        json={
            "id": id,
            "eventer_name": "Updated Eventer", 
            "eventer_info": "This is an updated eventer"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["eventer_name"] == "Updated Eventer"
    assert data["eventer_info"] == "This is an updated eventer"
    assert data["id"] == id

@patch.object(EventerRepository, 'delete_eventer')
def test_delete_eventer(mock_delete_eventer):
    id = str(uuid4())
    mock_delete_eventer.return_value = {}
    
    response = client.delete(f"/eventer/delete/{id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data == {}

@patch.object(EventerRepository, 'search_eventers')
def test_search_eventers(mock_search_eventers):
    mock_search_eventers.return_value = [
        {
            "eventer_name": "Search Eventer 1",
            "eventer_info": "This is a search result eventer 1", 
            "id": str(uuid4())
        },
        {
            "eventer_name": "Search Eventer 2",
            "eventer_info": "This is a search result eventer 2", 
            "id": str(uuid4())
        }
    ]
    
    response = client.get("/eventer/search?eventer_name=Search Eventer")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["eventer_name"] == "Search Eventer 1"
    assert data[1]["eventer_name"] == "Search Eventer 2"
