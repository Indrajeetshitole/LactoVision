# LactoVision — Integrated project setup

## Status and limitations

This package integrates the existing FastAPI/MongoDB application with the saved Phase 5 Random Forest pipeline, prediction history, rule-based recommendations and alerts, analytics, and CSV reporting. Static syntax checks were performed during packaging. **Live MongoDB connectivity, end-to-end browser workflows, and deployment have not been verified in your environment.** No real-world model accuracy is claimed: training data is synthetic.

## 1. Security

The ZIP intentionally does not contain `.env` secrets. Rotate any previously exposed MongoDB password and JWT secret. Never commit them. Configure a MongoDB Atlas IP access rule for your current IP.

## 2. Backend (from project root)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your private MongoDB URI, database name, and a long random JWT secret. Do not share it publicly. Start from project root:

```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

Check http://127.0.0.1:8000/api/health and http://127.0.0.1:8000/docs . Database endpoints need working MongoDB credentials.

## 3. Frontend (second terminal)

```bash
cd frontend
cp .env.example .env
npm ci
npm run dev
```

Open http://localhost:5173 . Register/login, create a farm and a cow, then use **Prediction**. Enter measured animal, feed, health and environmental inputs. The model expects the same features as Phase 5; missing fields are handled by its saved imputation pipeline where supported. The UI does not invent measurements. Results and alerts are stored in your existing MongoDB database.

## 4. Available APIs

- `GET /api/predict/fields` — supported model features (requires login)
- `POST /api/predict` — authenticated prediction and history storage; JSON `{ "cow_id": "<MongoDB cow document id>", "inputs": {"breed": "Holstein", ...} }`
- `GET /api/predictions` — saved predictions
- `GET /api/recommendations` — rule-based advice from predictions
- `GET /api/alerts` — saved risk alerts
- `GET /api/dashboard/summary` — live user-scoped counts and mean predicted yield
- `GET /api/analytics/milk-trend` — recorded daily milk totals
- `GET /api/reports/predictions.csv` — user-scoped CSV export

Existing authentication, farms, cattle, milk, feed, health and environment routes are preserved.

## 5. Important validation checklist

- MongoDB ping succeeds; user registration/login succeeds.
- Farm and cow CRUD works with the signed-in user.
- Model loads without scikit-learn version warnings.
- Prediction form submits with realistic inputs and returns a numeric prediction.
- Saved prediction is visible after page refresh.
- Recommendations and alerts appear only when triggered by input rules.
- Analytics reflect actual MongoDB records; CSV exports contain the signed-in user's predictions.
- Verify predictions on held-out cows and eventually real farm data before any operational use.

## 6. Not yet implemented/verified

Automated PDF report generation, robust model calibration and real-farm validation, comprehensive automated API/browser tests, deployment infrastructure, and clinically validated health-risk prediction are not provided. Do not present rule-based alerts as veterinary diagnoses or optimization as scientifically proven.
