from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..database import get_database
from ..schemas.phase3 import FeedCreate, FeedResponse
from ..security import get_current_user

router = APIRouter(prefix="/feed", tags=["Feed & Nutrition"])


def oid(value: str, label: str):
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid {label}")
    return ObjectId(value)


def ensure_cow(cow_id: str, user_id: str):
    if get_database()["cows"].find_one({"_id": oid(cow_id, "cow id"), "user_id": ObjectId(user_id)}) is None:
        raise HTTPException(status_code=404, detail="Cow not found or not owned by current user")


def response(doc):
    return FeedResponse(id=str(doc["_id"]), user_id=str(doc["user_id"]), cow_id=str(doc["cow_id"]), date=doc["date"],
                        feed_type=doc["feed_type"], quantity=doc["quantity"], feeding_time=doc["feeding_time"],
                        nutrition_value=doc["nutrition_value"], notes=doc.get("notes", ""))


@router.post("", response_model=FeedResponse, status_code=status.HTTP_201_CREATED)
def create_feed(payload: FeedCreate, current_user=Depends(get_current_user)):
    ensure_cow(payload.cow_id, current_user["id"])
    doc = payload.model_dump()
    doc["cow_id"] = oid(payload.cow_id, "cow id")
    doc["user_id"] = ObjectId(current_user["id"])
    doc["created_at"] = datetime.now(timezone.utc)
    result = get_database()["feed_records"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return response(doc)


@router.get("/{cow_id}", response_model=list[FeedResponse])
def cow_feed(cow_id: str, current_user=Depends(get_current_user)):
    ensure_cow(cow_id, current_user["id"])
    docs = get_database()["feed_records"].find({"cow_id": oid(cow_id, "cow id"), "user_id": ObjectId(current_user["id"])}).sort([("date", -1), ("created_at", -1)])
    return [response(doc) for doc in docs]


@router.get("", response_model=list[FeedResponse])
def list_feed(cow_id: str | None = Query(default=None), current_user=Depends(get_current_user)):
    query = {"user_id": ObjectId(current_user["id"])}
    if cow_id:
        ensure_cow(cow_id, current_user["id"])
        query["cow_id"] = oid(cow_id, "cow id")
    docs = get_database()["feed_records"].find(query).sort([("date", -1), ("created_at", -1)])
    return [response(doc) for doc in docs]
