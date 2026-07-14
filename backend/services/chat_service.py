import os

from openai import OpenAI

from services.tour_service import _load_tours

SYSTEM_PROMPT = (
    "당신은 대전·충청권 관광 정보를 안내하는 챗봇입니다. "
    "제공된 관광지, 문화시설, 축제, 레포츠, 숙박, 쇼핑, 음식점 정보를 바탕으로 "
    "사용자의 질문에 친절하고 간결하게 답변하세요. "
    "실제로 존재하는 장소만 추천하고, 모르는 정보는 모른다고 답하세요."
)

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")
        _client = OpenAI(api_key=api_key)
    return _client


def _find_references(reply: str, limit: int = 3) -> list[dict]:
    references = []
    for tour in _load_tours():
        title = tour.get("title", "")
        if title and title in reply:
            references.append(
                {
                    "contentid": tour.get("contentid", ""),
                    "title": title,
                    "addr1": tour.get("addr1", ""),
                    "firstimage": tour.get("firstimage", ""),
                }
            )
        if len(references) >= limit:
            break
    return references


def get_chat_reply(message: str, history: list[dict]) -> tuple[str, list[dict]]:
    client = _get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend({"role": h["role"], "content": h["content"]} for h in history)
    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(model=model, messages=messages)
    except Exception as exc:
        raise RuntimeError(f"OpenAI 호출 실패: {exc}") from exc

    reply = completion.choices[0].message.content or ""
    references = _find_references(reply)
    return reply, references
