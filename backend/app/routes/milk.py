from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..database import get_database
from ..schemas.phase3 import MilkCreate, MilkResponse
from ..security import get_current_user

router = APIRouter(prefix="/milk", tags=["Milk"])


def oid(value: str, label: str):
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid {label}")
    return ObjectId(value)


def ensure_cow(cow_id: str, user_id: str):
    cow = get_database()["cows"].find_one({"_id": oid(cow_id, "cow id"), "user_id": ObjectId(user_id)})
    if cow is None:
        raise HTTPException(status_code=404, detail="Cow not found or not owned by current user")
    return cow


def response(doc):
    return MilkResponse(id=str(doc["_id"]), user_id=str(doc["user_id"]), cow_id=str(doc["cow_id"]),
                        date=doc["date"], morning_milk=doc["morning_milk"], evening_milk=doc["evening_milk"],
                        total_milk=doc["total_milk"], notes=doc.get("notes", ""))


@router.post("", response_model=MilkResponse, status_code=status.HTTP_201_CREATED)
def create_milk(payload: MilkCreate, current_user=Depends(get_current_user)):
    ensure_cow(payload.cow_id, current_user["id"])
    now = datetime.now(timezone.utc)
    doc = payload.model_dump()
    doc["cow_id"] = oid(payload.cow_id, "cow id")
    doc["user_id"] = ObjectId(current_user["id"])
    doc["total_milk"] = round(payload.morning_milk + payload.evening_milk, 3)
    doc["created_at"] = now
    result = get_database()["milk_records"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return response(doc)


@router.get("", response_model=list[MilkResponse])
def list_milk(cow_id: str | None = Query(default=None), current_user=Depends(get_current_user)):
    query = {"user_id": ObjectId(current_user["id"])}
    if cow_id:
        ensure_cow(cow_id, current_user["id"])
        query["cow_id"] = oid(cow_id, "cow id")
    docs = get_database()["milk_records"].find(query).sort([("date", -1), ("created_at", -1)])
    return [response(doc) for doc in docs]


@router.get("/{cow_id}", response_model=list[MilkResponse])
def cow_milk(cow_id: str, current_user=Depends(get_current_user)):
    ensure_cow(cow_id, current_user["id"])
    docs = get_database()["milk_records"].find({"cow_id": oid(cow_id, "cow id"), "user_id": ObjectId(current_user["id"])}).sort("date", -1)
    return [response(doc) for doc in docs]
