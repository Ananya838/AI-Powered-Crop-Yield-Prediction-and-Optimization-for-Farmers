from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from fastapi import WebSocket
from starlette.websockets import WebSocketState


@dataclass
class ConnectionInfo:
    user_id: int | None = None
    role: str = "farmer"
    district: str | None = None
    rooms: set[str] = field(default_factory=set)


class WebSocketManager:
    def __init__(self) -> None:
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)
        self.connections: dict[WebSocket, ConnectionInfo] = {}

    async def connect(self, websocket: WebSocket, room: str, info: ConnectionInfo | None = None) -> None:
        await websocket.accept()
        self.rooms[room].add(websocket)
        connection_info = info or ConnectionInfo()
        connection_info.rooms.add(room)
        self.connections[websocket] = connection_info

    def add_room(self, websocket: WebSocket, room: str) -> None:
        self.rooms[room].add(websocket)
        self.connections.setdefault(websocket, ConnectionInfo()).rooms.add(room)

    def update(self, websocket: WebSocket, **fields: Any) -> None:
        connection = self.connections.setdefault(websocket, ConnectionInfo())
        for key, value in fields.items():
            setattr(connection, key, value)

    def get_info(self, websocket: WebSocket) -> ConnectionInfo:
        return self.connections.get(websocket, ConnectionInfo())

    def disconnect(self, websocket: WebSocket) -> None:
        connection = self.connections.pop(websocket, None)
        if connection:
            for room in list(connection.rooms):
                self.rooms[room].discard(websocket)
                if not self.rooms[room]:
                    self.rooms.pop(room, None)

    async def send_json(self, websocket: WebSocket, payload: dict[str, Any]) -> None:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(payload)

    async def broadcast(self, room: str, payload: dict[str, Any]) -> None:
        for websocket in list(self.rooms.get(room, set())):
            try:
                await self.send_json(websocket, payload)
            except Exception:
                self.disconnect(websocket)
