# API Documentation

Base URL: `http://localhost:8000/api/v1`

## Auth

### POST `/auth/register`
Request:
```json
{
  "full_name": "Farmer Name",
  "phone": "9876543210",
  "password": "secure123",
  "language": "en"
}
```

### POST `/auth/login`
Request:
```json
{
  "phone": "9876543210",
  "password": "secure123"
}
```
Response:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Yield Prediction

### POST `/prediction/yield`
Headers: `Authorization: Bearer <jwt>`

Input fields:
- crop, district, village
- rainfall, temperature
- nitrogen, phosphorus, potassium, ph
- irrigation, season

Response fields:
- expected_yield
- confidence_score
- suggested_crop
- yield_trend
- explainability

### POST `/prediction/explain`
Headers: `Authorization: Bearer <jwt>`

Returns top feature impacts from SHAP (or fallback contribution map).

## Smart Optimization

### POST `/optimization/plan`
Headers: `Authorization: Bearer <jwt>`

Response:
- irrigation_schedule
- fertilizer_dosage
- sowing_date
- harvest_window
- pest_prevention
- disease_risk_alerts
- crop_rotation_advice
- expected_gain_percent

## Pest Risk

### GET `/pest/risk?crop=wheat&humidity=72&temperature=30`
Headers: `Authorization: Bearer <jwt>`

## External Data Sources

### GET `/data/weather?district=Pune&season=kharif`
Headers: `Authorization: Bearer <jwt>`

Returns weather summary from Open-Meteo with Redis caching and fallback mode.

### GET `/data/soil?latitude=18.52&longitude=73.85`
Headers: `Authorization: Bearer <jwt>`

Returns soil summary from SoilGrids with fallback mode.

## Admin Analytics

### GET `/admin/analytics`
Headers: `Authorization: Bearer <admin-jwt>`

Returns district heatmap, productivity report, failure alerts, and adoption analytics.
