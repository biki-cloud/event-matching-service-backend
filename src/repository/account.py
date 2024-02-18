from typing import List
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource

from logging import getLogger

logger = getLogger(__name__)

class AccountRepository:
    def __init__(self, db: ServiceResource, table_name: str) -> None:
        self.__db = db
        self.__table = self.__db.Table(table_name)

    def get_all_accounts(self) -> List[dict]:
        response = self.__table.scan()
        return response.get('Items', [])

    def get_account(self, id: str) -> dict:
        try:
            response = self.__table.get_item(Key={'id': id})
            return response['Item']
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def register_account(self, account: dict) -> dict:
        response = self.__table.put_item(Item=account)
        logger.error(f"AccountRepository.register_account: {response}")
        return response

    def update_account(self, account: dict) -> dict:
        response = self.__table.update_item(
            Key={'id': account.get('id')},
            UpdateExpression="""
                set
                    first_name=:first_name,
                    last_name=:last_name,
                    email=:email,
                    password=:password,
                    roles=:roles
            """,
            ExpressionAttributeValues={
                ':id': account.get('id'),
                ':first_name': account.get('first_name'),
                ':last_name': account.get('last_name'),
                ':email': account.get('email'),
                ':password': account.get('password'),
                ':roles': account.get('roles')
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_account(self, id: str) -> dict:
        response = self.__table.delete_item(
            Key={'id': id}
        )
        return response
    
    def search_accounts(self, account_name: str) -> List[dict]:
        response = self.__table.scan(
            FilterExpression="contains(account_name, :query)",
            ExpressionAttributeValues={":query": account_name}
        )
        return response.get('Items', [])
    
    def get_account_by_email(self, email: str) -> dict:
        response = self.__table.scan(
            FilterExpression="email = :email",
            ExpressionAttributeValues={":email": email}
        )
        return response.get('Items', [])

    def get_me(self, email: str) -> dict:
        response = self.__table.scan(
            FilterExpression="email = :email",
            ExpressionAttributeValues={":email": email}
        )
        return response.get('Items', [])
