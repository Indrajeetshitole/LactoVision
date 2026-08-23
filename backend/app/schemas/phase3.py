from pydantic import BaseModel, Field
from typing import Optional


class MilkCreate(BaseModel):
    cow_id: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    morning_milk: float = Field(ge=0)
    evening_milk: float = Field(ge=0)
    notes: Optional[str] = Field(default="", max_length=500)


class MilkResponse(MilkCreate):
    id: str
    user_id: str
    total_milk: float


class FeedCreate(BaseModel):
    cow_id: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    feed_type: str = Field(min_length=1, max_length=120)
    quantity: float = Field(gt=0)
    feeding_time: str = Field(min_length=1, max_length=20)
    nutrition_value: float = Field(ge=0)
    notes: Optional[str] = Field(default="", max_length=500)


class FeedResponse(FeedCreate):
    id: str
    user_id: str


class HealthCreate(BaseModel):
    cow_id: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    temperature: float = Field(gt=20, lt=50)
    symptoms: Optional[str] = Field(default="", max_length=500)
    appetite: str = Field(min_length=1, max_length=50)
    activity: str = Field(min_length=1, max_length=50)
    health_status: str = Field(min_length=1, max_length=80)
    vaccination: Optional[str] = Field(default="", max_length=300)
    treatment: Optional[str] = Field(default="", max_length=500)
    notes: Optional[str] = Field(default="", max_length=500)


class HealthResponse(HealthCreate):
    id: str
    user_id: str


class EnvironmentCreate(BaseModel):
    farm_id: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    temperature: float = Field(gt=-50, lt=70)
    humidity: float = Field(ge=0, le=100)


class EnvironmentResponse(EnvironmentCreate):
    id: str
    user_id: str
