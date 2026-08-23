from datetime import datetime
from pydantic import BaseModel, Field


class TestRecordCreate(BaseModel):
    message: str = Field(min_length=1, max_length=200)


class TestRecordResponse(BaseModel):
    id: str
    message: str
    created_at: datetime
