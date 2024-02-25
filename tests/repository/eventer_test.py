"""
EventerRepositoryのテスト
mock_dynamodbを使ってdynamodbのモックを作成し、テストを実行する
リポジトリが正常にdynamodbを操作できるかを確認する
"""
import boto3
from uuid import uuid4

from moto import mock_dynamodb
from src.repository.eventer_repository import EventerRepository

@mock_dynamodb
def test_get_all_eventers():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='eventer',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    eventer_repository = EventerRepository(dynamodb_mock, 'eventer')
    result = eventer_repository.get_all_eventers()
    assert result == []

@mock_dynamodb
def test_register_eventer():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='eventer',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    eventer_repository = EventerRepository(dynamodb_mock, 'eventer')
    eventer = {
        "id": str(uuid4()),
        "eventer_name": "Test Eventer",
        "eventer_info": "This is a test eventer"
    }
    result = eventer_repository.register_eventer(eventer)
    assert result

@mock_dynamodb
def test_update_eventer():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='eventer',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    eventer_repository = EventerRepository(dynamodb_mock, 'eventer')
    eventer = {
        "id": str(uuid4()),
        "eventer_name": "Updated Eventer",
        "eventer_info": "This is an updated test eventer"
    }
    result = eventer_repository.update_eventer(eventer)
    assert result

@mock_dynamodb
def test_delete_eventer():
    dynamodb_mock = boto3.resource('dynamodb', region_name='us-west-2')
    dynamodb_mock.create_table(
        TableName='eventer',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    eventer_repository = EventerRepository(dynamodb_mock, 'eventer')
    id = str(uuid4())
    result = eventer_repository.delete_eventer(id)
    assert result