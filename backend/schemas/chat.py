from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class ChatReference(BaseModel):
    contentid: str
    title: str
    addr1: str
    firstimage: str


class ChatResponse(BaseModel):
    reply: str
    references: list[ChatReference]
