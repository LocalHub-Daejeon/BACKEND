import os
import time
from datetime import datetime, timedelta

import requests

DAEJEON_NX = 67
DAEJEON_NY = 100

PTY_LABELS = {
    "0": "없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "4": "소나기",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림",
}

_CACHE_TTL_SECONDS = 600
_cache: dict | None = None
_cache_time: float = 0.0


def _latest_base_datetime(now: datetime) -> tuple[str, str]:
    if now.minute < 45:
        now -= timedelta(hours=1)
    return now.strftime("%Y%m%d"), now.strftime("%H00")


def _fetch_ultra_srt_ncst() -> dict:
    service_key = os.getenv("KMA_SERVICE_KEY_DECODED")
    if not service_key:
        raise RuntimeError("KMA_SERVICE_KEY_DECODED가 설정되지 않았습니다.")

    endpoint = os.getenv(
        "KMA_API_ENDPOINT", "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
    )
    base_date, base_time = _latest_base_datetime(datetime.now())

    response = requests.get(
        f"{endpoint}/getUltraSrtNcst",
        params={
            "serviceKey": service_key,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": DAEJEON_NX,
            "ny": DAEJEON_NY,
            "numOfRows": 10,
            "pageNo": 1,
        },
        timeout=5,
    )
    response.raise_for_status()
    body = response.json()["response"]

    result_code = body["header"]["resultCode"]
    if result_code != "00":
        raise RuntimeError(f"기상청 API 오류: {body['header']['resultMsg']}")

    items = body["body"]["items"]["item"]
    values = {item["category"]: item["obsrValue"] for item in items}

    return {
        "base_date": base_date,
        "base_time": base_time,
        "temperature": float(values["T1H"]),
        "humidity": int(values["REH"]),
        "wind_speed": float(values["WSD"]),
        "precipitation_type": PTY_LABELS.get(values["PTY"], "알 수 없음"),
    }


def get_daejeon_weather() -> dict:
    global _cache, _cache_time

    if _cache is not None and time.monotonic() - _cache_time < _CACHE_TTL_SECONDS:
        return _cache

    weather = _fetch_ultra_srt_ncst()
    _cache = weather
    _cache_time = time.monotonic()
    return weather
