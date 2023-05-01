from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.comment.utils import get_user_websocket

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connections in self.active_connections:
            await connections.send_text(message)


manager = ConnectionManager()


@router.websocket('/ws/{identifier}')
async def websocket_endpoint(websocket: WebSocket, identifier: int):
    user = await get_user_websocket(websocket)
    print(user)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f'You wrote: {data}', websocket)
            await manager.broadcast(f"Session №{identifier}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Session №{identifier} closed")
