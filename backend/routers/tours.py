from fastapi import APIRouter, HTTPException, Query

from schemas.tour import TourDetail, TourListResponse
from services import tour_service

router = APIRouter(prefix="/tours", tags=["tours"])


@router.get("", response_model=TourListResponse)
def list_tours(
    keyword: str | None = Query(default=None),
    content_type_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
):
    items, total = tour_service.search_tours(
        keyword=keyword, content_type_id=content_type_id, page=page, size=size
    )
    return TourListResponse(items=items, page=page, size=size, total=total)


@router.get("/{content_id}", response_model=TourDetail)
def get_tour_detail(content_id: str):
    tour = tour_service.get_tour_by_id(content_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="관광 정보를 찾을 수 없습니다.")
    return tour
