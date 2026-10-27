# Phase 4 and current training instructions

Phase 4 dataset preparation/EDA files are retained for traceability. For the currently selected Phase 5 workflow, train **Random Forest Regression only** from the project root:

```bash
python -m pip install -r ai/requirements-phase5.txt
python -m ai.src.train_random_forest
```

Do not run the legacy `train_sklearn.py`, `train_keras.py`, or `select_best.py` scripts for this single-model workflow. The Phase 5 script saves the model, test metrics, feature importance, and training metadata. See `PHASE5_RANDOM_FOREST.md`.
