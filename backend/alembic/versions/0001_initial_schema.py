"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-04-14 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False, unique=True),
        sa.Column("language", sa.String(length=20), nullable=False, server_default="en"),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "farms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("farm_name", sa.String(length=120), nullable=False),
        sa.Column("district", sa.String(length=80), nullable=False),
        sa.Column("village", sa.String(length=80), nullable=False),
        sa.Column("area_hectare", sa.Float(), nullable=False),
        sa.Column("irrigation_type", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "soil_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("farm_id", sa.Integer(), sa.ForeignKey("farms.id"), nullable=False),
        sa.Column("nitrogen", sa.Float(), nullable=False),
        sa.Column("phosphorus", sa.Float(), nullable=False),
        sa.Column("potassium", sa.Float(), nullable=False),
        sa.Column("ph", sa.Float(), nullable=False),
        sa.Column("organic_carbon", sa.Float()),
        sa.Column("moisture", sa.Float()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "weather_cache",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("district", sa.String(length=80), nullable=False),
        sa.Column("season", sa.String(length=30), nullable=False),
        sa.Column("avg_rainfall_mm", sa.Float(), nullable=False),
        sa.Column("avg_temperature_c", sa.Float(), nullable=False),
        sa.Column("raw_payload", sa.Text()),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "yield_predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("farm_id", sa.Integer(), sa.ForeignKey("farms.id")),
        sa.Column("crop", sa.String(length=80), nullable=False),
        sa.Column("season", sa.String(length=30), nullable=False),
        sa.Column("predicted_yield", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("suggested_crop", sa.String(length=80)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "pest_alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("district", sa.String(length=80), nullable=False),
        sa.Column("crop", sa.String(length=80), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("advisory", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("farm_id", sa.Integer(), sa.ForeignKey("farms.id")),
        sa.Column("irrigation_schedule", sa.Text(), nullable=False),
        sa.Column("fertilizer_dosage", sa.Text(), nullable=False),
        sa.Column("sowing_date", sa.String(length=30), nullable=False),
        sa.Column("harvest_window", sa.String(length=30), nullable=False),
        sa.Column("rotation_advice", sa.Text()),
        sa.Column("expected_gain_percent", sa.Float(), nullable=False, server_default="10"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "crop_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("district", sa.String(length=80), nullable=False),
        sa.Column("crop", sa.String(length=80), nullable=False),
        sa.Column("season", sa.String(length=30), nullable=False),
        sa.Column("yield_per_hectare", sa.Float(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "district_stats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("district", sa.String(length=80), nullable=False, unique=True),
        sa.Column("avg_productivity", sa.Float(), nullable=False),
        sa.Column("adoption_rate", sa.Float(), nullable=False),
        sa.Column("failure_alert_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("district_stats")
    op.drop_table("crop_history")
    op.drop_table("recommendations")
    op.drop_table("pest_alerts")
    op.drop_table("yield_predictions")
    op.drop_table("weather_cache")
    op.drop_table("soil_reports")
    op.drop_table("farms")
    op.drop_table("users")
