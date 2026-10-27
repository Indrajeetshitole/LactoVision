# Backend Integration – Phase 4

Do not replace the existing FastAPI application. Import the Phase 4 router into the existing `backend/app/main.py`.

The AI package is the sibling directory `ai/` at the LactoVision project root. Start FastAPI from the project root so Python can import `ai`:

```bash
cd LactoVision
python -m uvicorn backend.app.main:app --reload --port 8000
```

If the existing backend is already packaged differently, keep its current startup command and ensure the project root is on `PYTHONPATH`.

## Route

`POST /api/predict`

The request schema is implemented in `ai/src/api_model.py`.

## Integration pattern

Inside the existing backend `main.py`:

```python
from ai.src.api_model import router as ai_prediction_router
app.include_router(ai_prediction_router, prefix="/api")
```

The route loads the saved `best_model.pkl`, runs the same preprocessing pipeline embedded in the sklearn model, produces the prediction, and generates conservative decision-support recommendations.

## MongoDB

The existing project's MongoDB connection should be reused. After receiving the result, insert a document into an existing/new collection such as `milk_predictions` using the same `get_database()` helper already used by the Phase 2/3 routes. Store:

- authenticated user id
- cattle/farm id when available
- input parameters
- predicted milk yield
- model name
- recommendations
- alerts
- timestamp

Do not create a second MongoDB database.

## Important

The endpoint must not be enabled in production until a final six-model selection has been completed. During development, if `best_model.pkl` is missing it returns HTTP 503 rather than a fake prediction.
