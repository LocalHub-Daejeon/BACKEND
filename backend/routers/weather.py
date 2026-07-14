from fastapi import APIRouter, HTTPException

from schemas.weather import WeatherResponse
from services.weather_service import get_daejeon_weather

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("", response_model=WeatherResponse)
def get_weather():
    try:
        return get_daejeon_weather()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
