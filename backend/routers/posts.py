from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from models.post import Post
from schemas.post import (
    PostCreate,
    PostDelete,
    PostListResponse,
    PostResponse,
    PostUpdate,
)
from services.security import hash_password, verify_password

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PostListResponse)
def list_posts(
    keyword: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Post)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(Post.title.like(like), Post.content.like(like)))

    total = query.count()
    items = (
        query.order_by(Post.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return PostListResponse(items=items, page=page, size=size, total=total)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    post.view_count += 1
    db.commit()
    db.refresh(post)
    return post


@router.post("", response_model=PostResponse, status_code=201)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    post = Post(
        title=payload.title,
        content=payload.content,
        password_hash=hash_password(payload.password),
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if not verify_password(payload.password, post.password_hash):
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    post.title = payload.title
    post.content = payload.content
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, payload: PostDelete, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if not verify_password(payload.password, post.password_hash):
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()
    return {"message": "게시글이 삭제되었습니다."}


@router.post("/{post_id}/likes")
def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    post.like_count += 1
    db.commit()
    db.refresh(post)
    return {"post_id": post.id, "like_count": post.like_count}
