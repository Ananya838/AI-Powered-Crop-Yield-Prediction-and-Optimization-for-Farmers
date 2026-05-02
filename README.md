# AI-Powered Crop Yield Prediction and Optimization for Farmers

Production-ready full-stack platform for SIH 2025 Problem Statement 25044: "AI-Powered Crop Yield Prediction and Optimization".

This standalone project helps small-scale farmers improve productivity by 10%+ through:
- Crop yield prediction
- Irrigation optimization
- Fertilizer recommendation
- Pest-risk alerts
- Multilingual and voice-assisted interaction

## Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Recharts
- i18next
- Web Speech API

### Backend
- FastAPI
- SQLAlchemy
- JWT authentication
- MySQL
- Redis cache

### ML Pipeline
- Linear Regression, Random Forest, XGBoost (yield prediction)
- Prophet-ready weather insight integration
- Pest-risk classifier
- Hybrid rule + ML recommendation engine

## Repository Structure

```
backend/
	app/
		api/routes/
		core/
		models/
		schemas/
		services/
		ml/
	sql/init.sql
	requirements.txt
	Dockerfile

frontend/
	src/
		pages/
		components/
		layouts/
		api/
		styles/
	package.json
	Dockerfile

ml/
	train_yield_model.py
	pest_prediction.py
	recommendation_engine.py
	data/
	models/

docs/
	API_DOCS.md
	PPT_POINTS.md
	DEMO_SCRIPT.md

docker-compose.yml
```

## MySQL Schema Tables

Implemented tables:
- users
- farms
- soil_reports
- weather_cache
- yield_predictions
- pest_alerts
- recommendations
- crop_history
- district_stats

Schema SQL: `backend/sql/init.sql`

## Core Features

### 1) Yield Prediction
Input:
- crop, district, village
- rainfall, temperature
- NPK, pH
- irrigation, season

Output:
- expected yield
- confidence score
- trend graph points
- alternative crop suggestion

### 2) Smart Farm Optimization
Generates:
- irrigation schedule
- fertilizer dosage
- sowing date
- harvest window
- pest prevention
- disease risk alerts
- crop rotation advice

### 3) Admin Dashboard
- district productivity insights
- productivity reports
- crop failure alerts
- farmer adoption analytics

## Local Development

### 1) Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Database workflow:
```
cd backend
python scripts/seed_data.py
alembic upgrade head
python -m pytest -q
```

### 2) Frontend
```
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 3) ML Training
```
python ml/train_yield_model.py
python ml/pest_prediction.py
```

## Docker Deployment

Run complete stack:
```
docker compose up --build
```

Services:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- FastAPI docs: http://localhost:8000/docs
- MySQL: localhost:3306
- Redis: localhost:6379

## Key API Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/prediction/yield`
- `POST /api/v1/prediction/explain`
- `POST /api/v1/optimization/plan`
- `GET /api/v1/pest/risk`
- `GET /api/v1/data/weather`
- `GET /api/v1/data/soil`
- `GET /api/v1/admin/analytics`

Detailed API references: `docs/API_DOCS.md`

## SIH Assets

- PPT talking points: `docs/PPT_POINTS.md`
- Demo flow script: `docs/DEMO_SCRIPT.md`

## Production Readiness Notes

- Modular service architecture in backend
- JWT auth and role-gated admin analytics
- MySQL schema aligned with required entities
- Redis integration point for weather and predictions cache
- Live weather integration with Open-Meteo and Redis caching
- Soil data integration with SoilGrids and resilient fallback responses
- SHAP-ready explainability endpoint for transparent AI decisions
- Containerized deployment with Docker Compose
- CI pipeline for backend syntax and frontend build

## Next Enhancements

- Integrate live weather APIs with district geo mapping
- Add SHAP plots endpoint for model explainability
- Add background jobs for periodic model retraining
- Add offline-first mobile PWA mode for low-connectivity rural areas