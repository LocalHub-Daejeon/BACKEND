import os
import time
from datetime import datetime, timedelta

import requests

REGION_PREFIXES = ("대전", "세종", "충청남도", "충청북도")

_CACHE_TTL_SECONDS = 24 * 60 * 60
_cache: list[dict] | None = None
_cache_time: float = 0.0


def _fetch_page(service_key: str, endpoint: str, event_start_date: str, page_no: int) -> tuple[list[dict], int]:
    try:
        response = requests.get(
            f"{endpoint}/searchFestival2",
            params={
                "serviceKey": service_key,
                "MobileOS": "ETC",
                "MobileApp": "TourCommunity",
                "_type": "json",
                "eventStartDate": event_start_date,
                "numOfRows": 100,
                "pageNo": page_no,
                "arrange": "A",
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"TourAPI 호출 실패: {exc}") from exc

    body = response.json()["response"]

    result_code = body["header"]["resultCode"]
    if result_code != "0000":
        raise RuntimeError(f"TourAPI 오류: {body['header']['resultMsg']}")

    items = body["body"]["items"]
    if items == "":
        return [], 0

    item_list = items["item"]
    if isinstance(item_list, dict):
        item_list = [item_list]

    return item_list, body["body"]["totalCount"]


def _fetch_all_festivals() -> list[dict]:
    service_key = os.getenv("TOUR_API_SERVICE_KEY_DECODED")
    if not service_key:
        raise RuntimeError("TOUR_API_SERVICE_KEY_DECODED가 설정되지 않았습니다.")

    endpoint = os.getenv("TOUR_API_ENDPOINT", "https://apis.data.go.kr/B551011/KorService2")
    event_start_date = datetime.now().strftime("%Y%m%d")

    collected: list[dict] = []
    page_no = 1
    while True:
        items, total_count = _fetch_page(service_key, endpoint, event_start_date, page_no)
        collected.extend(items)
        if not items or len(collected) >= total_count:
            break
        page_no += 1

    return collected


def _to_calendar_event(item: dict) -> dict | None:
    addr1 = item.get("addr1", "")
    if not addr1.startswith(REGION_PREFIXES):
        return None

    start_raw = item.get("eventstartdate", "")
    end_raw = item.get("eventenddate", "")
    if not start_raw or not end_raw:
        return None

    start_date = datetime.strptime(start_raw, "%Y%m%d")
    end_date = datetime.strptime(end_raw, "%Y%m%d") + timedelta(days=1)

    return {
        "id": item.get("contentid", ""),
        "title": item.get("title", ""),
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"),
        "extendedProps": {
            "addr1": addr1,
            "firstimage": item.get("firstimage", ""),
            "tel": item.get("tel", ""),
        },
    }


def get_festivals() -> list[dict]:
    global _cache, _cache_time

    if _cache is not None and time.monotonic() - _cache_time < _CACHE_TTL_SECONDS:
        return _cache

    raw_items = _fetch_all_festivals()
    events = [event for item in raw_items if (event := _to_calendar_event(item)) is not None]

    _cache = events
    _cache_time = time.monotonic()
    return events
