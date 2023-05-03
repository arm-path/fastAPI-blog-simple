from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.comment.utils import get_user_websocket, get_article_websocket, insert_comment_db

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data: dict):
        for connections in self.active_connections:
            await connections.send_json(data)


manager = ConnectionManager()


@router.websocket('/ws/{identifier}/{id_article}')
async def websocket_endpoint(websocket: WebSocket, identifier: int, id_article):
    await manager.connect(websocket)
    try:
        while True:
            user = await get_user_websocket(websocket)
            article = await get_article_websocket(id_article)
            text = await websocket.receive_text()
            if user['status'] != 200:
                await manager.send_personal_message(
                    {'status': 403, 'error': 'You are not authorized!'}, websocket)
            if article['status'] != 200:
                await manager.send_personal_message(
                    {'status': 404, 'error': 'Failed to get article for comment'}, websocket)
            if user['status'] == 200 and article['status'] == 200:
                user_model = user['data'][0]['user']
                article_model = article['data'][0]['article']
                comment = await insert_comment_db(user_model, article_model, text)
                await manager.broadcast({'status': 200, 'id': comment.id, 'user': user_model.email, 'text': text})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
