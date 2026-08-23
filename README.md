# LactoVision – Phase 3

Phase 3 adds the real **Milk + Feed + Health + Environmental Data Modules** to the Phase 2 authentication, farm and cattle foundation.

## Backend APIs

### Milk
- `POST /api/milk`
- `GET /api/milk`
- `GET /api/milk/{cow_id}`
- Fields: `cow_id`, `date`, `morning_milk`, `evening_milk`, `total_milk`, `notes`
- `total_milk` is calculated automatically as morning + evening.

### Feed
- `POST /api/feed`
- `GET /api/feed`
- `GET /api/feed/{cow_id}`
- Fields: `cow_id`, `date`, `feed_type`, `quantity`, `feeding_time`, `nutrition_value`, `notes`

### Health
- `POST /api/health`
- `GET /api/health/{cow_id}`
- Fields: `cow_id`, `date`, `temperature`, `symptoms`, `appetite`, `activity`, `health_status`, `vaccination`, `treatment`, `notes`

### Environment
- `POST /api/environment`
- `GET /api/environment`
- Fields: `temperature`, `humidity`, `date`, `farm_id`

All Phase 3 data routes are protected by JWT and verify that the referenced cow/farm belongs to the authenticated user.

## MongoDB collections

Phase 3 uses:
- `milk_records`
- `feed_records`
- `health_records`
- `environment_records`

Existing collections remain:
- `users`
- `farms`
- `cows`
- `predictions`
- `recommendations`
- `alerts`
- `notifications`

## Run

### Backend
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Phase 3 test sequence

1. Login to an existing account or register one.
2. Create a farm.
3. Add at least one cow to that farm.
4. Open **Milk Records** and save morning/evening milk. Verify `total_milk` is calculated by the backend.
5. Open **Feed & Nutrition** and save a feed record.
6. Open **Health Monitoring**, select a cow and save a health record.
7. Open **Environment** and save temperature/humidity for a farm.
8. Refresh each page and confirm the records are loaded from MongoDB.
9. Verify the four Phase 3 collections in MongoDB.
10. Verify that a cow/farm from another user cannot be referenced.

## Phase boundary

No machine-learning predictions are generated in Phase 3. Dataset preparation and preprocessing begin in Phase 4, where milk yield is treated as a regression target.
# LactoVision
