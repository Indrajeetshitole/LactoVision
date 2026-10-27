# Dataset Status

The supplied `LactoVision_Master_Dataset_50000.csv`, `LactoVision_Train_40000.csv`, and `LactoVision_Test_10000.csv` identify their source as `LactoVision_Synthetic_Integrated_Training_v1`.

Therefore this Phase 4 implementation must describe the supplied dataset as **synthetic/integrated project data**, not as real-world farm data.

The train/test split supplied by the project is preserved:
- Train: 40,000 rows
- Test: 10,000 rows
- Master: 50,000 rows for EDA/overview

The Data Dictionary marks `daily_milk_yield_kg` as the target and the requested reporting/leakage columns as reporting-only. The ML feature matrix follows the feature groups in the Phase 4 implementation prompt and excludes identifiers and reporting-only milk/revenue/profit columns.
