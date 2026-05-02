from pydantic import BaseModel


class DistrictHeatmapPoint(BaseModel):
    district: str
    productivity_index: float


class AdminAnalyticsResponse(BaseModel):
    district_heatmap: list[DistrictHeatmapPoint]
    productivity_report: list[dict]
    crop_failure_alerts: list[dict]
    farmer_adoption: list[dict]
