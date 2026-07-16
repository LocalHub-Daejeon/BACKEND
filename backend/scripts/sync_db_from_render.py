"""Render에 배포된 백엔드의 posts 데이터를 가져와 로컬 tour_community.db에 반영한다.

사용법: backend 디렉터리에서 `python scripts/sync_db_from_render.py` 실행
"""

import sqlite3
from pathlib import Path

import requests

RENDER_BASE_URL = "https://backend-33kp.onrender.com"
DB_PATH = Path(__file__).resolve().parent.parent / "tour_community.db"
PLACEHOLDER_PASSWORD = "0000"


def fetch_all_posts(base_url: str) -> list[dict]:
    posts: list[dict] = []
    page = 1
    while True:
        response = requests.get(
            f"{base_url}/api/posts", params={"page": page, "size": 100}, timeout=10
        )
        response.raise_for_status()
        body = response.json()
        posts.extend(body["items"])
        if len(posts) >= body["total"]:
            break
        page += 1
    return posts


def main():
    posts = fetch_all_posts(RENDER_BASE_URL)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM posts")
    cur.executemany(
        """
        INSERT INTO posts
            (id, category, title, content, password, view_count, like_count, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                p["id"],
                p["category"],
                p["title"],
                p["content"],
                PLACEHOLDER_PASSWORD,
                p["view_count"],
                p["like_count"],
                p["created_at"].replace("T", " "),
                p["updated_at"].replace("T", " "),
            )
            for p in posts
        ],
    )
    con.commit()
    con.close()

    print(f"{len(posts)}건 동기화 완료 (password는 API에 노출되지 않아 '{PLACEHOLDER_PASSWORD}'로 채움)")


if __name__ == "__main__":
    main()
