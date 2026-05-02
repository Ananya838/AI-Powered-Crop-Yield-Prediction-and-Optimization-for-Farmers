from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.crop_history import CropHistory
from app.models.district_stat import DistrictStat


def admin_analytics_snapshot(db: Session) -> dict:
    district_rows = db.query(DistrictStat).order_by(DistrictStat.avg_productivity.desc()).all()
    crop_history_rows = db.query(CropHistory).order_by(CropHistory.year.asc()).all()

    if district_rows:
        district_heatmap = [
            {"district": row.district, "productivity_index": round(float(row.avg_productivity), 2)}
            for row in district_rows
        ]
        farmer_adoption = [
            {
                "district": row.district,
                "active_farmers": int(max(1, row.adoption_rate * 10)),
            }
            for row in district_rows
        ]
        crop_failure_alerts = [
            {"district": row.district, "alerts": int(row.failure_alert_count)} for row in district_rows if row.failure_alert_count > 0
        ]
    else:
        district_heatmap = [
            {"district": "Pune", "productivity_index": 78.2},
            {"district": "Nashik", "productivity_index": 82.4},
            {"district": "Nagpur", "productivity_index": 69.7},
        ]
        farmer_adoption = [
            {"district": "Pune", "active_farmers": 620},
            {"district": "Nashik", "active_farmers": 510},
        ]
        crop_failure_alerts = [
            {"district": "Nagpur", "alerts": 4},
            {"district": "Solapur", "alerts": 2},
        ]

    if crop_history_rows:
        productivity_report = [
            {
                "month": f"Y{row.year}",
                "avg_yield": round(float(row.yield_per_hectare), 2),
            }
            for row in crop_history_rows[-6:]
        ]
    else:
        productivity_report = [
            {"month": "Jan", "avg_yield": 2.8},
            {"month": "Feb", "avg_yield": 3.0},
            {"month": "Mar", "avg_yield": 3.1},
        ]

    return {
        "district_heatmap": district_heatmap,
        "productivity_report": productivity_report,
        "crop_failure_alerts": crop_failure_alerts,
        "farmer_adoption": farmer_adoption,
    }
