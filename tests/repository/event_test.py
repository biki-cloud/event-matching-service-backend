"""
mock_dynamodbを使ってdynamodbのモックを作成し、テストを実行する
リポジトリが正常にdynamodbを操作できるかを確認する
"""
import boto3
from uuid import uuid4

from moto import mock_dynamodb
from src.repository.event_repository import EventRepository

# mock_dynamodbをアノテーションで使用することで関数内で作成したdynamodbリソースはモックになる
@mock_dynamodb
def test_get_all_event():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='event',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    event_repository = EventRepository(dynamodb_mock, 'event')
    result = event_repository.get_all()
    assert result == []

@mock_dynamodb
def test_register_event():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='event',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    event_repository = EventRepository(dynamodb_mock, 'event')
    event = {
        "id": str(uuid4()),
        "event_name": "Test Event",
        "event_info": "This is a test event",
        "event_state": "draft"
    }
    result = event_repository.register_event(event)
    assert result

@mock_dynamodb
def test_update_event():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='event',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    event_repository = EventRepository(dynamodb_mock, 'event')
    event = {
        "id": str(uuid4()),
        "event_name": "Updated Event",
        "event_info": "This is an updated test event",
        "event_state": "open"
    }
    result = event_repository.update_event(event)
    assert result

@mock_dynamodb
def test_delete_event():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='event',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    event_repository = EventRepository(dynamodb_mock, 'event')
    id = str(uuid4())
    result = event_repository.delete_event(id)
    assert result