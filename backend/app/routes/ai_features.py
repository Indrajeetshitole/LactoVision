"""Authenticated milk-yield predictions, history, alerts, and analytics."""
from datetime import datetime, timezone
import csv
import io
import math

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, create_model

from ..database import get_database
from ..security import get_current_user
from ai.src.config import FEATURES, NUMERICAL_FEATURES
from ai.src.predict import load_best
from ai.src.recommendations import generate_recommendations

router = APIRouter(tags=["AI Predictions & Analytics"])

# The model expects all training-time features. Optional missing fields are
# filled with the pipeline's trained imputation defaults, not fabricated measurements.
PredictionFields = create_model("PredictionFields", **{
    key: (float | None if key in NUMERICAL_FEATURES else str | None, None)
    for key in FEATURES
})

class PredictionInput(BaseModel):
    cow_id: str
    inputs: PredictionFields


def owned_cow(cow_id: str, user_id: str):
    if not ObjectId.is_valid(cow_id):
        raise HTTPException(400, "Invalid cow ID")
    doc = get_database()["cows"].find_one({"_id": ObjectId(cow_id), "user_id": ObjectId(user_id)})
    if doc is None:
        raise HTTPException(404, "Cow not found or not owned by current user")
    return doc


def serialize(doc):
    return {
        "id": str(doc["_id"]), "cow_id": str(doc["cow_id"]),
        "predicted_milk_yield_kg": doc["predicted_milk_yield_kg"],
        "model_used": doc["model_used"],
        "recommendations": doc.get("recommendations", []),
        "health_alerts": doc.get("health_alerts", []),
        "created_at": doc["created_at"].isoformat(),
    }


@router.get("/predict/fields")
def prediction_fields(user=Depends(get_current_user)):
    return {"features": FEATURES, "numerical_features": NUMERICAL_FEATURES,
            "required": ["breed", "age_years", "body_weight_kg", "days_in_milk", "feed_quantity_kg_dm", "water_intake_l", "health_status", "ambient_temperature_c", "relative_humidity_pct"]}


@router.post("/predict")
def predict(payload: PredictionInput, user=Depends(get_current_user)):
    cow = owned_cow(payload.cow_id, user["id"])
    inputs = payload.inputs.model_dump(exclude_none=True)
    if not inputs:
        raise HTTPException(422, "At least one model input is required")
    try:
        import pandas as pd
        model, name = load_best()
        # Pipelines trained in Phase 5 include their own fitted imputers.
        frame = pd.DataFrame([{key: inputs.get(key) for key in FEATURES}])
        prediction = float(model.predict(frame[FEATURES])[0])
        if not math.isfinite(prediction):
            raise ValueError("Model produced a non-finite prediction")
    except FileNotFoundError as exc:
        raise HTTPException(503, "Trained model is unavailable") from exc
    except Exception as exc:
        raise HTTPException(422, f"Model could not process the supplied inputs: {exc}") from exc
    recommendations, alerts = generate_recommendations(inputs, prediction)
    now = datetime.now(timezone.utc)
    doc = {"user_id": ObjectId(user["id"]), "cow_id": cow["_id"],
           "inputs": inputs, "predicted_milk_yield_kg": round(prediction, 3),
           "model_used": name, "recommendations": recommendations,
           "health_alerts": alerts, "created_at": now}
    result = get_database()["predictions"].insert_one(doc)
    doc["_id"] = result.inserted_id
    if alerts:
        get_database()["alerts"].insert_many([
            {"user_id": ObjectId(user["id"]), "cow_id": cow["_id"],
             "message": alert, "source": "rule_based", "created_at": now}
            for alert in alerts
        ])
    return serialize(doc)


@router.get("/predictions")
def history(user=Depends(get_current_user)):
    return [serialize(d) for d in get_database()["predictions"].find(
        {"user_id": ObjectId(user["id"])}).sort("created_at", -1).limit(200)]


@router.get("/recommendations")
def recommendations(user=Depends(get_current_user)):
    docs = get_database()["predictions"].find({"user_id": ObjectId(user["id"])}).sort("created_at", -1).limit(100)
    return [serialize(d) for d in docs if d.get("recommendations")]


@router.get("/alerts")
def alerts(user=Depends(get_current_user)):
    docs = get_database()["alerts"].find({"user_id": ObjectId(user["id"])}).sort("created_at", -1).limit(200)
    return [{"id": str(d["_id"]), "cow_id": str(d["cow_id"]), "message": d["message"],
             "created_at": d["created_at"].isoformat()} for d in docs]


@router.get("/dashboard/summary")
def summary(user=Depends(get_current_user)):
    db = get_database()
    query = {"user_id": ObjectId(user["id"])}
    predictions = list(db["predictions"].find(query, {"predicted_milk_yield_kg": 1}))
    mean = round(sum(d["predicted_milk_yield_kg"] for d in predictions) / len(predictions), 2) if predictions else None
    return {"farms": db["farms"].count_documents(query), "cows": db["cows"].count_documents(query),
            "milk_records": db["milk_records"].count_documents(query),
            "feed_records": db["feed_records"].count_documents(query),
            "health_records": db["health_records"].count_documents(query),
            "predictions": len(predictions), "average_predicted_yield_kg": mean,
            "alerts": db["alerts"].count_documents(query)}


@router.get("/analytics/milk-trend")
def milk_trend(user=Depends(get_current_user)):
    docs = get_database()["milk_records"].find({"user_id": ObjectId(user["id"])},
        {"date": 1, "total_milk": 1}).sort("date", 1)
    sums = {}
    for doc in docs:
        key = str(doc["date"])
        sums[key] = sums.get(key, 0) + float(doc.get("total_milk", 0))
    return [{"date": day, "total_milk_kg": round(total, 2)} for day, total in sorted(sums.items())]


@router.get("/reports/predictions.csv")
def export_predictions(user=Depends(get_current_user)):
    docs = get_database()["predictions"].find({"user_id": ObjectId(user["id"])}).sort("created_at", -1)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "cow_id", "predicted_milk_yield_kg", "model", "recommendations", "alerts"])
    for d in docs:
        writer.writerow([d["created_at"].isoformat(), str(d["cow_id"]), d["predicted_milk_yield_kg"],
                         d["model_used"], "; ".join(d.get("recommendations", [])),
                         "; ".join(d.get("health_alerts", []))])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=lactovision_predictions.csv"})
