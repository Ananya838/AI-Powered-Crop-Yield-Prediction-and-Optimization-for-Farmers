from __future__ import annotations

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import CropHistory, DistrictStat, Farm, SoilReport, User


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        admin = session.query(User).filter(User.phone == "9000000000").first()
        if not admin:
            admin = User(
                full_name="Admin Farmer",
                phone="9000000000",
                language="en",
                hashed_password=get_password_hash("admin123"),
                is_admin=True,
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)

        farm = session.query(Farm).filter(Farm.user_id == admin.id).first()
        if not farm:
            farm = Farm(
                user_id=admin.id,
                farm_name="Demo Farm",
                district="Pune",
                village="Hinjawadi",
                area_hectare=2.5,
                irrigation_type="drip",
            )
            session.add(farm)
            session.commit()
            session.refresh(farm)

        if not session.query(SoilReport).filter(SoilReport.farm_id == farm.id).first():
            session.add(
                SoilReport(
                    farm_id=farm.id,
                    nitrogen=68.0,
                    phosphorus=31.0,
                    potassium=29.0,
                    ph=6.5,
                    organic_carbon=0.72,
                    moisture=24.0,
                )
            )

        district_stats = [
            ("Pune", 78.2, 61.4, 1),
            ("Nashik", 82.4, 54.8, 0),
            ("Nagpur", 69.7, 41.2, 4),
            ("Solapur", 72.9, 48.6, 2),
        ]
        for district, productivity, adoption, alerts in district_stats:
            existing = session.query(DistrictStat).filter(DistrictStat.district == district).first()
            if not existing:
                session.add(
                    DistrictStat(
                        district=district,
                        avg_productivity=productivity,
                        adoption_rate=adoption,
                        failure_alert_count=alerts,
                    )
                )

        crop_rows = [
            ("Pune", "wheat", "rabi", 2.7, 2021),
            ("Pune", "wheat", "rabi", 2.9, 2022),
            ("Pune", "wheat", "rabi", 3.1, 2023),
            ("Pune", "wheat", "rabi", 3.2, 2024),
            ("Nashik", "millet", "kharif", 2.4, 2022),
            ("Nashik", "millet", "kharif", 2.8, 2023),
            ("Nashik", "millet", "kharif", 3.0, 2024),
            ("Nagpur", "cotton", "kharif", 1.9, 2022),
            ("Nagpur", "cotton", "kharif", 2.1, 2023),
            ("Nagpur", "cotton", "kharif", 2.2, 2024),
        ]
        for district, crop, season, value, year in crop_rows:
            existing = (
                session.query(CropHistory)
                .filter(CropHistory.district == district, CropHistory.crop == crop, CropHistory.year == year)
                .first()
            )
            if not existing:
                session.add(
                    CropHistory(
                        district=district,
                        crop=crop,
                        season=season,
                        yield_per_hectare=value,
                        year=year,
                    )
                )

        session.commit()
        print("Seed data created successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
