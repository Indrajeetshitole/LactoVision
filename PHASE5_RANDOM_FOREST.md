# LactoVision — Phase 5: Random Forest Regression

## What this folder includes
- Existing React/Vite frontend and FastAPI/MongoDB backend source from the supplied project ZIP.
- Existing Phase 4 AI preprocessing/configuration files and dataset documentation.
- Master dataset (50,000 rows), training split (40,000 rows), test split (10,000 rows), and data dictionary.
- Phase 5 Random Forest training script, saved fitted pipeline, evaluation metrics, feature importance, and training metadata.

## Train/retrain Phase 5
Run these commands from the `LactoVision` project root on macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ai/requirements-phase5.txt
python -m ai.src.train_random_forest
```

The supplied split has 160 cows in training and 40 different cows in testing. The training script checks for cow-ID overlap and stops if overlap is found. The test CSV is used only for evaluation, not fitting.

Outputs:
- `ai/models/random_forest_regression.pkl`
- `ai/models/best_model.pkl` (payload used by the existing `ai/src/predict.py` loader)
- `ai/outputs/phase5_random_forest_metrics.json`
- `ai/outputs/phase5_random_forest_metrics.csv`
- `ai/outputs/phase5_feature_importance.csv`
- `ai/outputs/phase5_training_metadata.json`

## Important limitations
1. The dataset source is labelled `LactoVision_Synthetic_Integrated_Training_v1`; it is synthetic, not validated real-farm data. Test metrics must not be presented as proof of real-world accuracy.
2. Phase 5 trains Random Forest only, as requested. It does not claim that all six models have been trained or compared in this package.
3. The saved model is trained and evaluated, but it is not yet connected to the existing backend and Prediction page. That is the next integration phase.
4. Database credentials are intentionally not included. Copy `.env.example` to `backend/.env` and supply your own rotated MongoDB credentials locally. Never commit or share `.env`.
5. The model artifact was generated with scikit-learn 1.8.0. Use the pinned Phase 5 requirements when loading it, or retrain in the target environment.

## Backend setup
```bash
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
# Edit backend/.env locally with your own MongoDB URI and a strong JWT secret.
python -m uvicorn backend.app.main:app --reload --port 8000
```

The backend may start even if MongoDB is not reachable, but database-backed features will not work until the connection is configured.

## Frontend setup
In a separate Terminal window:
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Set `VITE_API_URL=http://localhost:8000/api` in `frontend/.env.local` if needed.

## Security
The source archive included a populated backend `.env`. That file has been excluded from this packaged project. Rotate any credentials that were present in the original archive before reusing the database account.
