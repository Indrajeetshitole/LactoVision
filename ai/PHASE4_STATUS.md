# Phase 4 status — dataset preparation

Phase 4 deliverables included in this package:
- Master, training, and independent test CSV files (50,000 / 40,000 / 10,000 rows).
- Data dictionary and dataset verification/preprocessing scripts.
- EDA outputs and preprocessing configuration.
- Target column: `daily_milk_yield_kg`.
- Leakage-prone milk components and target-derived reporting fields are excluded from model features.

The current requested model-development path is **Phase 5: Random Forest Regression only**. Do not run legacy multi-model instructions for this selected workflow; use `PHASE5_RANDOM_FOREST.md` and `python -m ai.src.train_random_forest`.

The dataset is labeled `LactoVision_Synthetic_Integrated_Training_v1`. It is synthetic and does not establish real-farm accuracy.
