from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_database
from ..schemas.phase3 import HealthCreate, HealthResponse
from ..security import get_current_user

router = APIRouter(prefix="/health", tags=["Health Monitoring"])


def oid(value: str, label: str):
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid {label}")
    return ObjectId(value)


def ensure_cow(cow_id: str, user_id: str):
    if get_database()["cows"].find_one({"_id": oid(cow_id, "cow id"), "user_id": ObjectId(user_id)}) is None:
        raise HTTPException(status_code=404, detail="Cow not found or not owned by current user")


def response(doc):
    return HealthResponse(id=str(doc["_id"]), user_id=str(doc["user_id"]), cow_id=str(doc["cow_id"]), date=doc["date"],
                          temperature=doc["temperature"], symptoms=doc.get("symptoms", ""), appetite=doc["appetite"],
                          activity=doc["activity"], health_status=doc["health_status"], vaccination=doc.get("vaccination", ""),
                          treatment=doc.get("treatment", ""), notes=doc.get("notes", ""))


@router.post("", response_model=HealthResponse, status_code=status.HTTP_201_CREATED)
def create_health(payload: HealthCreate, current_user=Depends(get_current_user)):
    ensure_cow(payload.cow_id, current_user["id"])
    doc = payload.model_dump()
    doc["cow_id"] = oid(payload.cow_id, "cow id")
    doc["user_id"] = ObjectId(current_user["id"])
    doc["created_at"] = datetime.now(timezone.utc)
    result = get_database()["health_records"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return response(doc)


@router.get("/{cow_id}", response_model=list[HealthResponse])
def cow_health(cow_id: str, current_user=Depends(get_current_user)):
    ensure_cow(cow_id, current_user["id"])
    docs = get_database()["health_records"].find({"cow_id": oid(cow_id, "cow id"), "user_id": ObjectId(current_user["id"])}).sort([("date", -1), ("created_at", -1)])
    return [response(doc) for doc in docs]
