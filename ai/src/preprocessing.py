from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from .config import *


def load_train_test():
    train = pd.read_csv(DATASET_DIR / "LactoVision_Train_40000.csv")
    test = pd.read_csv(DATASET_DIR / "LactoVision_Test_10000.csv")
    return train, test


def quality_report(df, name):
    return {
        "dataset": name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "missing": {k: int(v) for k, v in df.isna().sum().items() if v},
        "target_missing": int(df[TARGET].isna().sum()),
    }


def build_preprocessors():
    cat = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
    ])
    num_scaled = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    num_unscaled = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])
    scaled = ColumnTransformer([
        ("num", num_scaled, NUMERICAL_FEATURES),
        ("cat", cat, CATEGORICAL_FEATURES),
    ])
    tree = ColumnTransformer([
        ("num", num_unscaled, NUMERICAL_FEATURES),
        ("cat", cat, CATEGORICAL_FEATURES),
    ])
    return scaled, tree


def prepare():
    train, test = load_train_test()
    required = set(FEATURES + [TARGET])
    for name, df in [("train", train), ("test", test)]:
        missing = sorted(required - set(df.columns))
        if missing:
            raise ValueError(f"{name} missing required columns: {missing}")

    # Remove exact duplicates only. Do not delete legitimate outliers.
    train_before = len(train)
    test_before = len(test)
    train = train.drop_duplicates().reset_index(drop=True)
    test = test.drop_duplicates().reset_index(drop=True)

    report = {
        "train": quality_report(train, "LactoVision_Train_40000.csv"),
        "test": quality_report(test, "LactoVision_Test_10000.csv"),
        "duplicates_removed": {
            "train": train_before - len(train),
            "test": test_before - len(test),
        },
        "feature_count": len(FEATURES),
        "features": FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "numerical_features": NUMERICAL_FEATURES,
        "leakage_excluded": LEAKAGE_COLUMNS,
        "identifiers_excluded": IDENTIFIER_COLUMNS,
    }
    PREPROCESS_DIR.mkdir(parents=True, exist_ok=True)
    (PREPROCESS_DIR / "preprocessing_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    X_train = train[FEATURES]
    y_train = train[TARGET]
    X_test = test[FEATURES]
    y_test = test[TARGET]
    return train, test, X_train, y_train, X_test, y_test

if __name__ == "__main__":
    train, test, *_ = prepare()
    print("Phase 4 preprocessing prepared.")
    print(f"Train rows: {len(train)}")
    print(f"Test rows: {len(test)}")
