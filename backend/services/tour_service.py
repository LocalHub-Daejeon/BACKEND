import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

CONTENT_TYPE_FILES = {
    "12": "대전_충청권_관광지.json",
    "14": "대전_충청권_문화시설.json",
    "15": "대전_충청권_축제공연행사.json",
    "25": "대전_충청권_여행코스.json",
    "28": "대전_충청권_레포츠.json",
    "32": "대전_충청권_숙박.json",
    "38": "대전_충청권_쇼핑.json",
    "39": "대전_충청권_음식점.json",
}

_tours_cache: list[dict] | None = None


def _load_tours() -> list[dict]:
    global _tours_cache
    if _tours_cache is not None:
        return _tours_cache

    tours: list[dict] = []
    for content_type_id, filename in CONTENT_TYPE_FILES.items():
        file_path = DATA_DIR / filename
        if not file_path.exists():
            continue
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        content_type = data.get("contentType", "")
        for item in data.get("items", []):
            item["contentType"] = content_type
            item.setdefault("contenttypeid", content_type_id)
            tours.append(item)

    _tours_cache = tours
    return tours


def search_tours(
    keyword: str | None = None,
    content_type_id: int | None = None,
    page: int = 1,
    size: int = 20,
) -> tuple[list[dict], int]:
    tours = _load_tours()

    if content_type_id is not None:
        type_id_str = str(content_type_id)
        tours = [t for t in tours if t.get("contenttypeid") == type_id_str]

    if keyword:
        keyword_lower = keyword.lower()
        tours = [
            t
            for t in tours
            if keyword_lower in t.get("title", "").lower()
            or keyword_lower in t.get("addr1", "").lower()
        ]

    total = len(tours)
    start = (page - 1) * size
    end = start + size
    return tours[start:end], total


def list_tours_for_map(
    keyword: str | None = None,
    content_type_id: int | None = None,
) -> list[dict]:
    tours = _load_tours()

    if content_type_id is not None:
        type_id_str = str(content_type_id)
        tours = [t for t in tours if t.get("contenttypeid") == type_id_str]

    if keyword:
        keyword_lower = keyword.lower()
        tours = [
            t
            for t in tours
            if keyword_lower in t.get("title", "").lower()
            or keyword_lower in t.get("addr1", "").lower()
        ]

    return tours


def get_tour_by_id(content_id: str) -> dict | None:
    tours = _load_tours()
    for tour in tours:
        if tour.get("contentid") == content_id:
            return tour
    return None
