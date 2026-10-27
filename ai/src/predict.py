from pathlib import Path
import joblib
import pandas as pd
from .config import *


def load_best():
    best = MODEL_DIR / "best_model.pkl"
    if not best.exists():
        raise FileNotFoundError("best_model.pkl does not exist. Run model training and selection first.")
    payload=joblib.load(best)
    return payload["model"], payload["model_name"]


def predict_milk_yield(input_data):
    model,name=load_best()
    frame=pd.DataFrame([input_data])
    missing=[c for c in FEATURES if c not in frame.columns]
    if missing: raise ValueError(f"Missing prediction fields: {missing}")
    value=float(model.predict(frame[FEATURES])[0])
    return {"predicted_milk_yield_kg":value,"model_used":name}
