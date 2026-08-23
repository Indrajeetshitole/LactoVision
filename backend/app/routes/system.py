from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from ..database import get_database, is_connected
from ..schemas.system import TestRecordCreate, TestRecordResponse

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/test-records", response_model=list[TestRecordResponse])
def list_test_records():
    if not is_connected():
        raise HTTPException(status_code=503, detail="MongoDB is not connected")

    collection = get_database()["phase1_test_records"]
    records = collection.find().sort("created_at", -1).limit(50)

    return [
        TestRecordResponse(
            id=str(record["_id"]),
            message=record["message"],
            created_at=record["created_at"],
        )
        for record in records
    ]


@router.post("/test-record", response_model=TestRecordResponse, status_code=201)
def create_test_record(payload: TestRecordCreate):
    if not is_connected():
        raise HTTPException(status_code=503, detail="MongoDB is not connected")

    now = datetime.now(timezone.utc)
    result = get_database()["phase1_test_records"].insert_one(
        {"message": payload.message, "created_at": now}
    )

    return TestRecordResponse(
        id=str(result.inserted_id),
        message=payload.message,
        created_at=now,
    )
