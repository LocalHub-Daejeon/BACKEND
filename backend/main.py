import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from database import Base, engine
from routers import chat, health, posts, tours, weather

Base.metadata.create_all(bind=engine)

app = FastAPI(title="지역 관광 정보 및 커뮤니티 서비스 API")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(tours.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
