from typing import Union, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from chat.models import ChatRoom, ChatRoom, CreateChatRoom, RequestChatMessage

from common.response import ResponseModel
from common.time import current_milli_time
from .ConnectionManager import manager
from .ChatManager import ChatManager,chatHistory_data, get_room
from chat import database

router = APIRouter(
    # prefix="/ws",
    tags=["ws"],
)

@router.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await ChatManager.message_proc(room_id, websocket)

@router.get("/api/chatroom")
async def get_chat_rooms():
    room = await database.retrieve_room()
    if room:
        return room

@router.post("/api/chatroom")
async def create_chat_room(room: CreateChatRoom):
    result = await database.create_room(room)
    room.users = [room.owner] + room.users
    if result:
        return ResponseModel({"id":result})
    return []

@router.api_route("/api/chatroom/{room_id}")
async def chat_rooms(room_id:str):
    return await database.retrieve_room_detail(room_id)
    
@router.get("/api/chatroom/{room_id}/history")
async def chat_rooms(room_id: str):
    result = await database.retrieve_message(room_id)
    return ResponseModel(result)
    
    
@router.post("/api/chatroom/{room_id}/history")
async def send_chat_message(room_id: str, message: RequestChatMessage):
    message.roomId = room_id
    message.timestamp = current_milli_time()
    result = await database.create_message(message)
    return ResponseModel(result)
    
@router.post("/api/chatroom/{room_id}/enter")
async def chat_rooms(room_id: str):
    if  room_id in chatHistory_data:
        return chatHistory_data[room_id]
    else :
        return []

@router.post("/api/chatroom/{room_id}/exit")
async def chat_rooms(room_id: str):
    if  room_id in chatHistory_data:
        return chatHistory_data[room_id]
    else :
        return []
    