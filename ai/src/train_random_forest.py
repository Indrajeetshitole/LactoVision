"""Phase 5: train and evaluate the LactoVision Random Forest model.

Run from the project root:
    python -m ai.src.train_random_forest

The supplied test set is never used for fitting. The supplied split has no cow IDs
in common between train and test, so the final test score evaluates unseen cows.
"""
from __future__ import annotations

import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from .config import (
    DATASET_DIR, MODEL_DIR, OUTPUT_DIR, PREPROCESS_DIR, TARGET, FEATURES,
    IDENTIFIER_COLUMNS, LEAKAGE_COLUMNS,
)
from .preprocessing import build_preprocessors

TRAIN_PATH = DATASET_DIR / "LactoVision_Train_40000.csv"
TEST_PATH = DATASET_DIR / "LactoVision_Test_10000.csv"
MODEL_PATH = MODEL_DIR / "random_forest_regression.pkl"
BEST_PATH = MODEL_DIR / "best_model.pkl"
METRICS_PATH = OUTPUT_DIR / "phase5_random_forest_metrics.json"
CSV_METRICS_PATH = OUTPUT_DIR / "phase5_random_forest_metrics.csv"
IMPORTANCE_PATH = OUTPUT_DIR / "phase5_feature_importance.csv"
METADATA_PATH = OUTPUT_DIR / "phase5_training_metadata.json"


def metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict:
    return {
        "MAE_kg": float(mean_absolute_error(y_true, y_pred)),
        "RMSE_kg": float(mean_squared_error(y_true, y_pred) ** 0.5),
        "R2": float(r2_score(y_true, y_pred)),
        "MAPE_percent": float((np.abs((y_true.to_numpy() - y_pred) / np.clip(np.abs(y_true.to_numpy()), 1e-8, None))).mean() * 100),
    }


def main() -> None:
    for folder in (MODEL_DIR, OUTPUT_DIR, PREPROCESS_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    print("Loading datasets...", flush=True)
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)
    print(f"Loaded train={train.shape}, test={test.shape}", flush=True)
    for label, frame in (("training", train), ("test", test)):
        if TARGET not in frame.columns:
            raise ValueError(f"{label} CSV is missing target column {TARGET!r}")
        missing = [col for col in FEATURES if col not in frame.columns]
        if missing:
            raise ValueError(f"{label} CSV is missing required model features: {missing}")
        if frame[TARGET].isna().any():
            raise ValueError(f"{label} CSV contains missing target values")

    print("Checking duplicates and cow split...", flush=True)
    train = train.drop_duplicates().reset_index(drop=True)
    test = test.drop_duplicates().reset_index(drop=True)

    train_cows = set(train["cow_id"].dropna().astype(str)) if "cow_id" in train else set()
    test_cows = set(test["cow_id"].dropna().astype(str)) if "cow_id" in test else set()
    overlap = sorted(train_cows & test_cows)
    if overlap:
        raise ValueError(
            f"Train/test cow leakage detected: {len(overlap)} cow IDs occur in both splits. "
            "Regenerate a cow-grouped split before training."
        )

    X_train, y_train = train[FEATURES], train[TARGET]
    X_test, y_test = test[FEATURES], test[TARGET]
    print(f"Using {len(FEATURES)} features; building preprocessor...", flush=True)
    _, tree_preprocessor = build_preprocessors()

    estimator = RandomForestRegressor(
        n_estimators=30,
        max_depth=14,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        n_jobs=2,
        random_state=42,
    )
    pipeline = Pipeline([
        ("preprocessor", tree_preprocessor),
        ("model", estimator),
    ])

    print("Fitting Random Forest...", flush=True)
    started = time.perf_counter()
    pipeline.fit(X_train, y_train)
    training_seconds = time.perf_counter() - started
    y_pred = pipeline.predict(X_test)
    result = metrics(y_test, y_pred)
    result.update({
        "model": "Random Forest Regression",
        "target": TARGET,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "train_unique_cows": int(len(train_cows)),
        "test_unique_cows": int(len(test_cows)),
        "train_test_cow_overlap": int(len(overlap)),
        "feature_count": int(len(FEATURES)),
        "training_seconds": round(training_seconds, 3),
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_note": "Synthetic integrated dataset; results are not real-farm validation.",
    })

    joblib.dump(pipeline, MODEL_PATH, compress=3)
    # Existing prediction loader expects a {model, model_name} payload.
    joblib.dump({"model": pipeline, "model_name": "Random Forest Regression"}, BEST_PATH, compress=3)

    try:
        names = pipeline.named_steps["preprocessor"].get_feature_names_out()
        values = pipeline.named_steps["model"].feature_importances_
        pd.DataFrame({"feature": names, "importance": values}).sort_values(
            "importance", ascending=False
        ).to_csv(IMPORTANCE_PATH, index=False)
    except Exception as exc:
        result["feature_importance_warning"] = str(exc)

    metadata = {
        "phase": 5,
        "model": "RandomForestRegressor",
        "parameters": estimator.get_params(),
        "target": TARGET,
        "features": FEATURES,
        "excluded_identifiers": IDENTIFIER_COLUMNS,
        "excluded_leakage_columns": LEAKAGE_COLUMNS,
        "categorical_features": [c for c in FEATURES if c in {
            "breed", "breed_group", "sex", "lactation_stage", "feed_type", "health_status",
            "disease_status", "disease_type", "symptoms", "vaccination_status", "treatment_status",
            "weather_condition", "season"
        }],
        "train_file": TRAIN_PATH.name,
        "test_file": TEST_PATH.name,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "train_unique_cows": int(len(train_cows)),
        "test_unique_cows": int(len(test_cows)),
        "train_test_cow_overlap": int(len(overlap)),
        "python_version": platform.python_version(),
        "scikit_learn_version": sklearn.__version__,
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "note": "Test set is used only for final evaluation, never for model fitting. Dataset is synthetic.",
    }

    METRICS_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    CSV_METRICS_PATH.write_text(pd.DataFrame([result]).to_csv(index=False), encoding="utf-8")
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("\nPHASE 5 — RANDOM FOREST TRAINING COMPLETE")
    print("=" * 48)
    print(f"Training rows: {len(train):,} | unique cows: {len(train_cows)}")
    print(f"Test rows:     {len(test):,} | unique cows: {len(test_cows)}")
    print(f"Cow overlap:   {len(overlap)}")
    print(f"Features:      {len(FEATURES)}")
    print(f"Training time: {training_seconds:.2f} seconds")
    print("\nIndependent test metrics:")
    for key in ("MAE_kg", "RMSE_kg", "R2", "MAPE_percent"):
        print(f"  {key}: {result[key]:.6f}")
    print("\nSaved model:", MODEL_PATH.relative_to(Path.cwd()))
    print("Saved prediction-loader artifact:", BEST_PATH.relative_to(Path.cwd()))
    print("Saved metrics:", METRICS_PATH.relative_to(Path.cwd()))
    print("Saved feature importance:", IMPORTANCE_PATH.relative_to(Path.cwd()))
    print("\nCaution: dataset is synthetic; these metrics do not establish real-world farm accuracy.")


if __name__ == "__main__":
    main()
