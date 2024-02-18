import os
import boto3
from boto3.resources.base import ServiceResource
# from pynamodb.settings import settings

class Config:
    # DB_REGION_NAME = os.getenv('DB_REGION_NAME')
    DB_REGION_NAME = "xx"
    # DB_ACCESS_KEY_ID = os.getenv('DB_ACCESS_KEY_ID')
    DB_ACCESS_KEY_ID = "xx"
    # DB_SECRET_ACCESS_KEY = os.getenv('DB_SECRET_ACCESS_KEY')
    DB_SECRET_ACCESS_KEY = "xx"

# # PynamoDBのグローバル設定
# settings.configure(region=Config.DB_REGION_NAME,  # 例: 'us-west-2'
#                    aws_access_key_id=Config.DB_ACCESS_KEY_ID,
#                    aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY,
#                    host='http://dynamodb-local:8000')  # ローカルDynamoDBのエンドポイント

def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
                         region_name=Config.DB_REGION_NAME,
                         aws_access_key_id=Config.DB_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY,
                         endpoint_url="http://dynamodb-local:8000"
                         )

    return ddb

