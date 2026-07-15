from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

PostCategory = Literal["자유", "맛집", "여행팁", "후기"]
DEFAULT_CATEGORY: PostCategory = "자유"


class PostCreate(BaseModel):
    category: PostCategory = DEFAULT_CATEGORY
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=100)


class PostUpdate(BaseModel):
    category: PostCategory = DEFAULT_CATEGORY
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=100)


class PostDelete(BaseModel):
    password: str = Field(..., min_length=1, max_length=100)


class PostResponse(BaseModel):
    id: int
    category: PostCategory
    title: str
    content: str
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PostListResponse(BaseModel):
    items: list[PostResponse]
    page: int
    size: int
    total: int
