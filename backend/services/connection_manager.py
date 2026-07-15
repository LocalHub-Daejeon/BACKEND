import asyncio

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.loop: asyncio.AbstractEventLoop | None = None

    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast_viewer_count()

    async def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)
        await self.broadcast_viewer_count()

    async def broadcast(self, message: dict) -> None:
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                pass

    async def broadcast_viewer_count(self) -> None:
        await self.broadcast(
            {"type": "viewer_count", "count": len(self.active_connections)}
        )

    def broadcast_from_sync(self, message: dict) -> None:
        if self.loop is None:
            return
        asyncio.run_coroutine_threadsafe(self.broadcast(message), self.loop)


manager = ConnectionManager()
