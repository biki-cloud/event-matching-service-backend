from logging import getLogger
from typing import List
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource

logger = getLogger(__name__)

class EventRepository:
    def __init__(self, db: ServiceResource, table_name: str) -> None:
        self.__db = db
        self.__table = self.__db.Table(table_name)

    def get_all(self) -> List[dict]:
        response = self.__table.scan()
        return response.get('Items', [])

    def get_event(self, id: str) -> dict:
        try:
            response = self.__table.get_item(Key={'id': id})
            return response['Item']
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])
    
    def get_event_by_eventer_id(self, eventer_id: str) -> List[dict]:
        response = self.__table.scan(
            FilterExpression="eventer_id = :eventer_id",
            ExpressionAttributeValues={":eventer_id": eventer_id}
        )
        return response.get('Items', [])

    def register_event(self, event: dict) -> dict:
        response = self.__table.put_item(Item=event)
        return response

    def update_event(self, event: dict) -> dict:
        event['id'] = str(event['id'])

        response = self.__table.update_item(
            Key={'id': event.get('id')},
            UpdateExpression="""
                set
                    info=:info,
                    #name=:name,
                    #state=:state
            """,
            ExpressionAttributeValues={
                ':info': event.get('info'),
                ':name': event.get('name'),
                ':state': event.get('state')
            },
            ExpressionAttributeNames={
                '#name': 'name',
                '#state': 'state'
            },
            ReturnValues="UPDATED_NEW"
        )
        return response


    def delete_event(self, id: str) -> dict:
        response = self.__table.delete_item(
            Key={'id': id}
        )
        return response
    
    def search_event(self, event_name: str) -> List[dict]:
        response = self.__table.scan(
            FilterExpression="contains(event_name, :query)",
            ExpressionAttributeValues={":query": event_name}
        )
        return response.get('Items', [])