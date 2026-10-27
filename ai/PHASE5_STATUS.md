# Phase 5 status — Random Forest Regression

**Status: trained and smoke-tested in the build environment.**

## Training setup
- Training records: 40,000
- Test records: 10,000
- Unique training cows: 160
- Unique test cows: 40
- Cow IDs shared across splits: 0
- Features: 40
- Model: RandomForestRegressor (30 trees, max depth 14, `max_features=sqrt`, random state 42)
- Training time in build environment: 5.63 seconds

## Independent test metrics
- MAE: 1.6275 kg/day
- RMSE: 2.0322 kg/day
- R²: 0.8941
- MAPE: 6.62%

These are measured results for the supplied synthetic dataset only. They are not proof of accuracy on real dairy farms.

## Artifacts
- `ai/models/random_forest_regression.pkl` — fitted pipeline
- `ai/models/best_model.pkl` — fitted pipeline in the format expected by `ai/src/predict.py`
- `ai/outputs/phase5_random_forest_metrics.json` and `.csv` — metrics
- `ai/outputs/phase5_feature_importance.csv` — feature importance
- `ai/outputs/phase5_training_metadata.json` — versions, features and parameters

## Scope boundary
Phase 5 is complete for the requested Random Forest model. The FastAPI router and React Prediction page are **not yet connected**; that belongs to the next integration phase.
