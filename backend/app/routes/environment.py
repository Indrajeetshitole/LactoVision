from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_database
from ..schemas.phase3 import EnvironmentCreate, EnvironmentResponse
from ..security import get_current_user

router = APIRouter(prefix="/environment", tags=["Environment"])


def oid(value: str, label: str):
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid {label}")
    return ObjectId(value)


def ensure_farm(farm_id: str, user_id: str):
    if get_database()["farms"].find_one({"_id": oid(farm_id, "farm id"), "user_id": ObjectId(user_id)}) is None:
        raise HTTPException(status_code=404, detail="Farm not found or not owned by current user")


def response(doc):
    return EnvironmentResponse(id=str(doc["_id"]), user_id=str(doc["user_id"]), farm_id=str(doc["farm_id"]),
                               date=doc["date"], temperature=doc["temperature"], humidity=doc["humidity"])


@router.post("", response_model=EnvironmentResponse, status_code=status.HTTP_201_CREATED)
def create_environment(payload: EnvironmentCreate, current_user=Depends(get_current_user)):
    ensure_farm(payload.farm_id, current_user["id"])
    doc = payload.model_dump()
    doc["farm_id"] = oid(payload.farm_id, "farm id")
    doc["user_id"] = ObjectId(current_user["id"])
    doc["created_at"] = datetime.now(timezone.utc)
    result = get_database()["environment_records"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return response(doc)


@router.get("", response_model=list[EnvironmentResponse])
def list_environment(current_user=Depends(get_current_user)):
    docs = get_database()["environment_records"].find({"user_id": ObjectId(current_user["id"])}).sort([("date", -1), ("created_at", -1)])
    return [response(doc) for doc in docs]
