from fastapi import APIRouter, HTTPException

from schemas.festival import FestivalEvent
from services.festival_service import get_festivals

router = APIRouter(prefix="/festivals", tags=["festivals"])


@router.get("", response_model=list[FestivalEvent])
def list_festivals():
    try:
        return get_festivals()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
