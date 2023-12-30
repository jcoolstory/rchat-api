from typing import List
from collections import defaultdict
from fastapi import WebSocket
from starlette.websockets import WebSocketState

class ConnectionManager:
    def __init__(self):
        self.sock_id_map = defaultdict(list)
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def add_user(self, websocket: WebSocket, id:str):
        if id not in self.sock_id_map:
            self.sock_id_map[id] = []
        
        self.sock_id_map[id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: any):
        await self.broadcast_target(message, self.active_connections)

    async def broadcast_target(self, message: any, connections:List[WebSocket]):
        for connection in connections:
            print(connection.client_state)
            try:
                if connection.client_state != WebSocketState.DISCONNECTED:
                    await connection.send_text(message)
                else:
                    print("socket closed")
            except:
                pass

    def get_socket_by_id(self, id: str):
        return self.sock_id_map[id]

manager = ConnectionManager()