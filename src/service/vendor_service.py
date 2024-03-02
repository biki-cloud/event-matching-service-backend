
from typing import List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class VendorModel(BaseModel):
    id: Union[UUID, None] = Field(default=None, description="出店者ID", example="123e4567-e89b-12d3-a456-426614174000")
    info: str = Field(description="出店者情報", example="お祭りだしてます")
    account_id: Union[UUID, None] = Field(default=None, description="出店者が紐付いているユーザーID", example="123e4567-e89b-12d3-a456-426614174000")
