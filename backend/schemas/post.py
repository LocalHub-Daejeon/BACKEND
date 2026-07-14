from datetime import datetime

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=100)


class PostUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=100)


class PostDelete(BaseModel):
    password: str = Field(..., min_length=1, max_length=100)


class PostResponse(BaseModel):
    id: int
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
